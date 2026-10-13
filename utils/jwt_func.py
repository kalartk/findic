from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from fastapi.security import OAuth2PasswordBearer

from model.user import get_user_id
from database.db import get_session
from model.models import User
from auth.auth import secret_key


auth_bearer = OAuth2PasswordBearer(tokenUrl="/auth/")

#decoder le jwt-token et retirer le user lier de la bdd
def get_header_user(token: Annotated[str, Depends(auth_bearer)], 
                    session:Session = Depends(get_session)
                    ) -> User:
    try:
        paylod = jwt.decode(jwt=token, key=secret_key, algorithms=["HS256"])
        user_id = paylod.get("id")

        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="missing credentials")
        
        user = get_user_id(user_id, session)

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="missing credentials")
        
        return user
    
    except jwt.PyJWTError:
        print("erreur de token")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not authenticated")
