from fastapi import Form, HTTPException, APIRouter
from auth import AuthHandler
from db.db import *

router = APIRouter()
auth_handler = AuthHandler()


@router.post("/user/register", status_code=201)
async def register(username: str = Form(""), password: str = Form("")):
    hashed_password = auth_handler.get_password_hash(password)
    query = 'INSERT INTO admins(name, password, created) VALUES (:name, :password, now())'
    values = {'name': username, "password": hashed_password}
    await db_conn.execute(query=query, values=values)
    return {"test": "I'M WORKING"}


@router.post("/user/login", status_code=200)
async def login(username: str = Form(""), password: str = Form("")):
    query = 'SELECT * FROM admins WHERE name = :username'
    values = {'username': username}
    user = await db_conn.fetch_one(query=query, values=values)
    hashed_password = auth_handler.get_password_hash(password)
    print(user.get("_id"), type(user.get("_id")))
    if user:
        if hashed_password == user.get('password'):
            token = auth_handler.encode_token(user.get('_id'))
            return {'token': token, 'username': user.get('name')}

    raise HTTPException(status_code=401, detail='Invalid username and/or password.')
