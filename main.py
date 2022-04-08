from os import getenv
from fastapi import FastAPI, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

import databases
import sql_queries
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

    data = await db.fetch_all(sql_queries.GET_CARGOS)

    return {"data": data}


@app.post("/cargos")
async def new_cargo(token=Depends(auth_handler.auth_wrapper),
                    name: str = Form(''),
                    weight: int = Form(0), weightunit: str = Form(''),
                    quantity: int = Form(0), quantityunit: str = Form(''),
                    info: str = Form(0)
                    ):
    if not auth_handler.get_session(token):
        raise HTTPException(status_code=440, detail='Session has expired')

    uid = auth_handler.get_session(token)

    values = {"name": name, "wth": weight, "wunit": weightunit,
              "qty": quantity, "qunit": quantityunit, "info": info, "uid": uid}
    await db.execute(query=sql_queries.NEW_CARGO, values=values)
    data = await db.fetch_all(sql_queries.GET_CARGOS)
    return {"data": data}


@app.get("/drivers")
async def get_drivers():
    # token = auth_handler.auth_wrapper
    # if not auth_handler.get_session(token):
    #     raise HTTPException(status_code=440, detail='Session has expired')

    data = await db.fetch_all(sql_queries.GET_DRIVERS)

    return {"data": data}


@app.post("/drivers")
async def new_driver(token= Depends(auth_handler.auth_wrapper),
                     firstname: str = Form(''),
                     lastname: str = Form(''),
                     phone: str = Form(''),
                     email: str = Form('')
                     ):

    if not auth_handler.get_session(token):
        raise HTTPException(status_code=440, detail='Session has expired')
    uid = auth_handler.get_session(token)
    values = {"fname": firstname, "lname": lastname, "ph": phone, "email": email, "uid": uid}
    await db.execute(query=sql_queries.NEW_DRIVER, values=values)
    data = await db.fetch_all(sql_queries.GET_DRIVERS)
    return {"data": data}


@app.get("/transports")
async def get_transports(token=Depends(auth_handler.auth_wrapper)):
    if not auth_handler.get_session(token):
        raise HTTPException(status_code=440, detail='Session has expired')

    trans = await db.fetch_all(sql_queries.GET_TRANSPORTS)
    data = []
    for t in trans:
        t = dict(t)
        values = [{"id": t['_id']}]
        statuses = await db.fetch_all(
            f"SELECT * FROM statuses WHERE transportid = {t['_id']}")
        t["statuses"] = statuses
        data.append(t)
    return {"data": data}
