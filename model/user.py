from fastapi import HTTPException, status
from sqlmodel import Session, select
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError

from model.models import User
from utils.pwd_bcrypt import hash_pwd_bcrypt

#Ajouter un utilisateur dans la bdd
def add_user(data: User, session:Session) -> User:
    utilisateur = data
    hash_mdp = hash_pwd_bcrypt(utilisateur.password)
    utilisateur.password = hash_mdp
    try:
        session.add(utilisateur)
        session.commit()
        session.refresh(utilisateur)
        
    except IntegrityError:
        session.rollback()
        print("erreur avec l'enregistrement | unique index")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="information déjà disponible")
        
    finally:
        session.close()

    return utilisateur

#Get user avec son email ou son pseudo
def get_user(value: str, session: Session) -> User|None:
    try:
        stmt = select(User).where((User.email == value) | (User.pseudo == value))
        user = session.exec(statement=stmt).first()
    finally:
        session.close()
    return user

def get_user_id(value: str, session: Session) -> User|None:
    try:
        user = session.get(User, value)
        return user
    finally:
        session.close()

