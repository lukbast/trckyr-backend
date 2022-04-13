from fastapi import Form, HTTPException, Depends, APIRouter
from auth import AuthHandler
from db.db import *

router = APIRouter()
auth_handler = AuthHandler()


@router.get("/drivers")
async def get_drivers(token=Depends(auth_handler.auth_wrapper)):
    data = await db_conn.fetch_all(GET_DRIVERS)

    return {"data": data}


@router.post("/drivers")
async def new_driver(token=Depends(auth_handler.auth_wrapper),
                     firstname: str = Form(''),
                     lastname: str = Form(''),
                     phone: str = Form(''),
                     email: str = Form('')
                     ):

    uid = auth_handler.decode_token(token)
    values = {"fname": firstname, "lname": lastname, "ph": phone, "email": email, "uid": uid}
    await db_conn.execute(query=NEW_DRIVER, values=values)
    data = await db_conn.fetch_all(GET_DRIVERS)
    return {"data": data}


@router.patch("/drivers/{_id}")
async def edit_driver(_id: int, token=Depends(auth_handler.auth_wrapper),
                      firstname: str = Form(''),
                      lastname: str = Form(''),
                      phone: str = Form(''),
                      email: str = Form('')
                      ):
    if not auth_handler.get_session(token):
        raise HTTPException(status_code=440, detail='Session has expired')
    uid = auth_handler.get_session(token)
    values = {"fname": firstname, "lname": lastname, "ph": phone, "email": email, "uid": uid, 'id': _id}
    await db_conn.execute(query=UPDATE_DRIVERS, values=values)
    data = await db_conn.fetch_all(GET_DRIVERS)
    return {"data": data}
