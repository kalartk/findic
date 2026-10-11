from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session
from model.user import bcrypt_context
from datetime import datetime, timedelta, timezone
from typing import Annotated

from model.user import get_user, get_user_id
from model.models import User
from config.config import Config
from database.db import get_session

app_auth = APIRouter()
app_auth.prefix = "/auth"

secret_key = Config.secret_key if Config.secret_key else "ZNSUusuzu236G25ed3"

auth_bearer = OAuth2PasswordBearer(tokenUrl="/auth/")

class Token(BaseModel):
    value: str
    type: str

@app_auth.post("/")
async def auth_user(data: Annotated[OAuth2PasswordRequestForm, Depends()],
                    session:Session = Depends(get_session)
                    ) -> Token:
    if data.username == "" or data.password == "" or not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="bad details")

    user = get_user(value=data.username, session=session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="bad details, not found")

    if not bcrypt_context.verify(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid credentials")

    date_heure = datetime.now(timezone.utc) + timedelta(minutes=30)

    payload = {"sub": user.pseudo, "id":user.id,"exp": date_heure}

    tkn = jwt_encoder(payload=payload)
    return Token(value=tkn, type="Bearer")


def jwt_encoder(payload):
    token = jwt.encode(claims=payload, key=secret_key, algorithm="HS256")
    return token


def get_header_user(token: Annotated[str, Depends(auth_bearer)], 
                    session:Session = Depends(get_session)
                    ) -> User:
    try:
        paylod = jwt.decode(token=token, key=secret_key, algorithms="HS256")
        user_id = paylod.get("id")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="missing credentials")
        user = get_user_id(user_id, session)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="missing credentials")
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not authenticated")
