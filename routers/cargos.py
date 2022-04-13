from fastapi import Form, HTTPException, Depends, APIRouter
from auth import AuthHandler
from db.db import *

router = APIRouter()
auth_handler = AuthHandler()


@router.get("/cargos")
async def get_cargos(token=Depends(auth_handler.auth_wrapper)):

    data = await db_conn.fetch_all(GET_CARGOS)

    return {"data": data}


@router.post("/cargos")
async def new_cargo(token=Depends(auth_handler.auth_wrapper),
                    name: str = Form(''),
                    weight: int = Form(0), weightunit: str = Form(''),
                    quantity: int = Form(0), quantityunit: str = Form(''),
                    info: str = Form('')
                    ):

    uid = auth_handler.get_session(token)
    values = {"name": name, "wth": weight, "wunit": weightunit,
              "qty": quantity, "qunit": quantityunit, "info": info, "uid": uid}
    await db_conn.execute(query=NEW_CARGO, values=values)
    data = await db_conn.fetch_all(GET_CARGOS)
    return {"data": data}


@router.patch("/cargos/{_id}")
async def edit_cargo(_id: int, token=Depends(auth_handler.auth_wrapper),
                     name: str = Form(''),
                     weight: int = Form(0), weightunit: str = Form(''),
                     quantity: int = Form(0), quantityunit: str = Form(''),
                     info: str = Form('')
                     ):

    uid = auth_handler.decode_token(token)
    values = {'name': name, 'w': weight, "wunit": weightunit,
              'q': quantity, 'qunit': quantityunit, 'uid': uid, 'info': info, "id": _id}
    await db_conn.execute(UPDATE_CARGO, values)
    data = await db_conn.fetch_all(GET_CARGOS)
    return {'data': data}
