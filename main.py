from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi.responses import JSONResponse

from user_client import app_user
from auth.auth import app_auth
from database.db import init_db
from depense_client import app_depense
from dette_client import app_dette
from avoir_client import app_avoir
from emprunt_client import app_emprunt

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=app_user)
app.include_router(router=app_auth)
app.include_router(router=app_depense)
app.include_router(router=app_dette)
app.include_router(router=app_avoir)
app.include_router(router=app_emprunt)

visite = 0

@app.get("/")
async def index():
    global visite
    visite += 1
    return {"bonjour":f"bonjour, vous etes le {visite} visiteur"}

#creer un handler pour raiser toutes les exceptions de sqlmodel et sqlachemy
@app.exception_handler(Exception)
async def exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": "Une erreur est survenue"}
    )