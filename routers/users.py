from fastapi import Form, HTTPException, Depends, APIRouter
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

    if user:
        if hashed_password == user.get('password'):
            token = auth_handler.encode_token(username)
            auth_handler.create_session(token, user.get('_id'))
            return {'token': token, 'username': user.get('name')}

    raise HTTPException(status_code=401, detail='Invalid username and/or password.')


@router.get("/user/login", status_code=200)
async def login_with_session(token=Depends(auth_handler.auth_wrapper)):
    session = auth_handler.get_session(token)
    if session:
        return {'session': True}

    raise HTTPException(status_code=440, detail='Session has ben expired')


@router.post("/user/logout", status_code=200)
async def logout(token=Depends(auth_handler.auth_wrapper)):
    auth_handler.remove_session(token)
    return {"logged_out": True}
