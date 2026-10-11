from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from sqlmodel import Session
from typing import Annotated

from model.user import add_user, get_user
from model.models import User
from database.db import get_session
from auth.auth import get_header_user

app_user = APIRouter(tags=['user'])
app_user.prefix = "/api"

class UserCreate(BaseModel):
    nom: str
    prenom: str
    email: str
    password: str
    pseudo: str | None = None

class UserGet(BaseModel):
    nom: str
    prenom: str
    email: str
    pseudo: str | None

@app_user.post("/user", status_code=status.HTTP_201_CREATED)
async def create_user(user:UserCreate, 
                      session:Session = Depends(get_session)
                      ) -> None:
    data = User(nom=user.nom, prenom=user.prenom, email=user.email, password=user.password, pseudo=user.pseudo)
    add_user(data, session=session)

@app_user.get("/user/{email_or_pseudo}", status_code=status.HTTP_200_OK)
async def get_user_email_pseudo(utilisateur: Annotated[User, Depends(get_header_user)],
                                session: Session = Depends(get_session)
                                )-> UserGet:
    user = utilisateur
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found or bad value")
    
    utils = UserGet(nom=user.nom, prenom=user.prenom, email=user.email, pseudo=user.pseudo)
    return utils