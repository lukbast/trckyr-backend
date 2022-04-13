from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Routes
from routers.users import router as users
from routers.cargos import router as cargos
from routers.drivers import router as drivers
from routers.transports import router as transports


from db.db import *
from auth import AuthHandler

auth_handler = AuthHandler()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(users)
app.include_router(cargos)
app.include_router(drivers)
app.include_router(transports)


@app.on_event("startup")
async def startup():
    await db_conn.connect()


@app.on_event("shutdown")
async def shutdown():
    await db_conn.disconnect()


@app.get("/")
async def root():
    return {"test": "I AM WORKING!"}
