from fastapi import Form, HTTPException, Depends, APIRouter
from auth import AuthHandler
from db.db import *
from uitls import calculate_distance, get_coordinates

router = APIRouter()
auth_handler = AuthHandler()


@router.get("/transports")
async def get_transports(token=Depends(auth_handler.auth_wrapper)):

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


@router.post("/transports")
async def new_transport(name: str = Form(''),
                        from_: str = Form(''),
                        to_: str = Form(''),
                        cargo: int = Form(0),
                        drivers: list[int] = Form(0),
                        token=Depends(auth_handler.auth_wrapper)):

    uid = auth_handler.decode_token(token)
    # Geocodes provided locations
    from_coors, to_coors = get_coordinates(from_, to_)

    # calculate distance between locations
    dist = calculate_distance(from_coors, to_coors)

    # push new transport to database
    values = {"name": name, "from": from_, "to": to_, "cargo": cargo, "drivers": drivers, "total": dist, "uid": uid}
    print(values)
    await db_conn.execute(NEW_TRANSPORT, values)

    # Gets ID of newly created transport
    id_ = await db_conn.fetch_one("SELECT max(_id) as id FROM transports;")
    id_ = id_["id"]

    # Pushes initial transport state to database
    values = {"id": id_, "rem_dist": dist, "eta": "1 day 09 hrs 23 mins", "from_coors": from_coors}
    await db_conn.execute(INITIAL_STATUS, values)
    return {'status': "ok"}
