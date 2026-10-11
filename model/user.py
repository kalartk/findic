from pwdlib import PasswordHash
from fastapi import HTTPException, status
from sqlmodel import Session, select

from model.models import User

bcrypt_context = PasswordHash.recommended()

def hash_pass(value: str) -> str:
    mdp = bcrypt_context.hash(value)
    return mdp

#Ajouter un utilisateur dans la bdd
def add_user(data: User, session:Session) -> User:
    utilisateur = data
    hash_mdp = hash_pass(utilisateur.password)
    utilisateur.password = hash_mdp
    try:
        session.add(utilisateur)
        session.commit()
        session.refresh(utilisateur)
    except IndexError:
        print("erreur avec l'enregistrement")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        
    finally:
        session.close()

    return utilisateur

#Get user avec son email ou son pseudo
def get_user(value: str, session: Session) -> User|None:
    try:
        stmt = select(User).where(User.email == value)
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

