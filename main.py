from fastapi import FastAPI
from contextlib import asynccontextmanager

from user_client import app_user
from auth.auth import app_auth
from database.db import init_db
from depense_client import app_depense
from dette_client import app_dette

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=app_user)
app.include_router(router=app_auth)
app.include_router(router=app_depense)
app.include_router(router=app_dette)

@app.get("/")
async def index():
    return {"bonjour":"toi"}