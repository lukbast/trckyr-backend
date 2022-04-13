from fastapi import Form, HTTPException, Depends, APIRouter
from auth import AuthHandler
from db.db import *

router = APIRouter()
auth_handler = AuthHandler()


@router.get("/transports")
async def get_transports(token=Depends(auth_handler.auth_wrapper)):
    if not auth_handler.get_session(token):
        raise HTTPException(status_code=440, detail='Session has expired')

    trans = await db_conn.fetch_all(GET_TRANSPORTS)
    data = []
    for t in trans:
        t = dict(t)
        values = [{"id": t['_id']}]
        statuses = await db_conn.fetch_all(
            f"SELECT * FROM statuses WHERE transportid = {t['_id']}")
        t["statuses"] = statuses
        data.append(t)
    return {"data": data}
