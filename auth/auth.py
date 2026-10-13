from fastapi.security import OAuth2PasswordRequestForm
import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session
from datetime import datetime, timedelta, timezone
from typing import Annotated

from model.user import get_user
from config.config import Config
from database.db import get_session
from utils.pwd_bcrypt import verify_pwd_hash

app_auth = APIRouter()
app_auth.tags = ['auth']
app_auth.prefix = "/auth"

secret_key = Config.secret_key if Config.secret_key else "ZNSUusuzu236G25ed3"

class Token(BaseModel):
    access_token: str
    token_type: str

@app_auth.post("/")
async def auth_user(data: Annotated[OAuth2PasswordRequestForm, Depends()],
                    session:Session = Depends(get_session)
                    ) -> Token:
    if data.username == "" or data.password == "" or not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="bad details")

    user = get_user(value=data.username, session=session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="bad details, not found")

    if not verify_pwd_hash(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid credentials")

    date_heure = datetime.now(timezone.utc) + timedelta(weeks=2)

    payload = {"sub": user.pseudo if user.pseudo else user.prenom, "id":user.id,"exp": date_heure}

    tkn = jwt_encoder(payload=payload)
    return Token(access_token=tkn, token_type="bearer")


def jwt_encoder(payload):
    token = jwt.encode(algorithm='HS256', key=secret_key, payload=payload)
    return token