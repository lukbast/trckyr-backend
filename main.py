from os import getenv
from fastapi import FastAPI, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

import databases
from auth import AuthHandler


def create_db_url(host: str, port: str, db_name: str, user: str,
                  password: str):
    return 'postgresql://{}:{}@{}:{}/{}'.format(
        user, password, host, port, db_name)


DB_URL = create_db_url(getenv("POSTGRES_URL"),
                       getenv("PORT"),
                       getenv("POSTGRES_DB"),
                       getenv("POSTGRES_USER"),
                       getenv("POSTGRES_PASSWORD"))
db = databases.Database(DB_URL)
auth_handler = AuthHandler()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.get("/")
async def root():
    return {"test": "I AM WORKING!"}


@app.post("/user/register", status_code=201)
async def register(username: str = Form(""), password: str = Form("")):
    hashed_password = auth_handler.get_password_hash(password)
    query = 'INSERT INTO admins(name, password, created) VALUES (:name, :password, now())'
    values = {'name': username, "password": hashed_password}
    await db.execute(query=query, values=values)
    return {"test": "I'M WORKING"}


@app.post("/user/login", status_code=200)
async def login(username: str = Form(""), password: str = Form("")):
    query = 'SELECT * FROM admins WHERE name = :username'
    values = {'username': username}
    user = await db.fetch_one(query=query, values=values)
    hashed_password = auth_handler.get_password_hash(password)

    if user:
        if hashed_password == user.get('password'):
            token = auth_handler.encode_token(username)
            auth_handler.create_session(token, user.get('_id'))
            return {'token': token, 'username': user.get('name')}

    raise HTTPException(status_code=401, detail='Invalid username and/or password.')


@app.get("/user/login", status_code=200)
async def loginWithSession(token=Depends(auth_handler.auth_wrapper)):
    session = auth_handler.get_session(token)
    if session:
        return {'session': True}

    raise HTTPException(status_code=440, detail='Session has ben expired')


@app.post("/user/logout", status_code=200)
async def logout(token=Depends(auth_handler.auth_wrapper)):
    auth_handler.remove_session(token)
    return {"logged_out": True}


@app.get("/cargos")
async def get_cargos(token=Depends(auth_handler.auth_wrapper)):
    if not auth_handler.get_session(token):
        raise HTTPException(status_code=440, detail='Session has expired')

    data = await db.fetch_all(
        "SELECT cargos._id, cargos.name, weight, weightUnit, quantity, "
        "quantityUnit, info, who_added.name as addedBy, cargos.added,  "
        "lastModified, who_mod.name as modifiedBy FROM cargos "
        "JOIN admins as who_added ON cargos.addedBy = who_added._id "
        "JOIN admins as who_mod ON cargos.modifiedBy = who_mod._id;")

    return {"data": data}


@app.get("/drivers")
async def get_drivers(token= Depends(auth_handler.auth_wrapper)):
    if not auth_handler.get_session(token):
        raise HTTPException(status_code=440, detail='Session has expired')

    data = await db.fetch_all(
        "SELECT drivers._id, firstname, lastname, who_added.name as addedby, added, "
        "lastmodified, phone, email, who_mod.name as modifiedby FROM drivers "
        "JOIN admins AS who_added ON drivers.addedBy = who_added._id "
        "JOIN admins AS who_mod ON drivers.modifiedBy = who_mod._id;")

    return {"data": data}


@app.get("/transports")
async def get_transports(token=Depends(auth_handler.auth_wrapper)):
    if not auth_handler.get_session(token):
        raise HTTPException(status_code=440, detail='Session has expired')

    trans = await db.fetch_all(
        "SELECT t._id, t.name, from_, to_, drivers, cargo, "
        "total, t.state, who_added.name as addedby, added, lastmodified, who_mod.name as modifiedby "
        "FROM transports as t "
        "JOIN admins AS who_added ON t.addedBy = who_added._id "
        "JOIN admins AS who_mod ON t.modifiedBy = who_mod._id;"
    )
    data = []
    for t in trans:
        t = dict(t)
        values = [{"id": t['_id']}]
        statuses = await db.fetch_all(
            f"SELECT * FROM statuses WHERE transportid = {t['_id']}")
        t["statuses"] = statuses
        data.append(t)
    return {"data": data}
