from os import getenv
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
import databases


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


@app.get("/cargos")
async def get_cargos():
    curr = await db.fetch_all(
        "SELECT cargos._id, cargos.name, weight, weightUnit, quantity, "
        "quantityUnit, info, who_added.name as addedBy, cargos.added,  "
        "lastModified, who_mod.name as modifiedBy FROM cargos "
        "JOIN admins as who_added ON cargos.addedBy = who_added._id "
        "JOIN admins as who_mod ON cargos.modifiedBy = who_mod._id;")

    return {"data": curr}
