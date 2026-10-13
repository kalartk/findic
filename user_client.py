from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from sqlmodel import Session
from typing import Annotated

from model.user import add_user, get_user
from model.models import User
from database.db import get_session
from utils.jwt_func import get_header_user

app_user = APIRouter(tags=['user'])

class UserCreate(BaseModel):
    nom: str
    prenom: str
    email: EmailStr
    password: str
    pseudo: str | None = None

class UserGet(BaseModel):
    nom: str | None
    prenom: str | None
    email: EmailStr
    pseudo: str | None

@app_user.post("/user", status_code=status.HTTP_201_CREATED)
async def create_user(user:UserCreate, 
                      session:Session = Depends(get_session)
                      ) -> None:
    data = User(nom=user.nom, prenom=user.prenom, email=user.email, password=user.password, pseudo=user.pseudo)
    add_user(data, session=session)

@app_user.get("/user/{email_or_pseudo}", status_code=status.HTTP_200_OK)
async def get_user_email_pseudo(email_or_pseudo: str,
                                utilisateur: Annotated[User, Depends(get_header_user)],
                                session: Session = Depends(get_session)
                                )-> UserGet:
    user = get_user(value=email_or_pseudo, session=session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found or bad value")

    if user != utilisateur:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="operation not allowed")
    
    utils = UserGet(nom=user.nom, prenom=user.prenom, email=user.email, pseudo=user.pseudo)
    return utils

    
    
