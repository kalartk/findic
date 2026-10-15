from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field
from typing import Annotated
from sqlmodel import Session
from uuid import UUID

from model.models import Emprunt, Devise, User
from model.emprunt import create_emprunt, get_emprunt, get_all_emprunt, update_emprunt, delete_emprunt
from database.db import get_session
from utils.jwt_func import get_header_user

app_emprunt = APIRouter(
    tags=['emprunt'],
    prefix="/emprunt"
)

class EmpruntCreate(BaseModel):
    user_id: int = Field(description="ID of the user")
    montant: float = Field(description="ID of the book")
    devise: Devise = Field(description="la devise/argent a utilise")
    proprio: str

class EmpruntUpdate(BaseModel):
    montant: float | None
    devise: Devise | None
    proprio: str | None
    status: bool


@app_emprunt.post("/", status_code=status.HTTP_201_CREATED)
async def create_emprunt_handler(data: EmpruntCreate,
                                 utilisateur: Annotated[User, Depends(get_header_user)],
                                 session: Annotated[Session, Depends(get_session)]
) -> dict[str,str]:

    create_emprunt(Emprunt(
        montant=data.montant,
        devise=data.devise,
        proprio=data.proprio,
        user_id=utilisateur.id,
        
    ), session)
    return {"message":"emprunt creer"}

@app_emprunt.get("/{id}", status_code=status.HTTP_200_OK)
async def get_emprunt_id(id: UUID,
                         utilisateur: Annotated[User, Depends(get_header_user)],
                         session: Annotated[Session, Depends(get_session)]
) -> Emprunt:
    emprunt = get_emprunt(id, session)
    if not emprunt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="emprunt non trouve")
    if emprunt.user_id != utilisateur.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="vous n'avez pas acces a cet emprunt")
    return emprunt

@app_emprunt.get("/all", status_code=status.HTTP_200_OK)
async def get_all_emprunt_id(utilisateur: Annotated[User, Depends(get_header_user)],
                             session: Annotated[Session, Depends(get_session)]
) -> list[Emprunt]:
    emprunt_list = get_all_emprunt(utilisateur.id, session)
    return emprunt_list

@app_emprunt.put("/{id}", status_code=status.HTTP_200_OK)
async def update_emprunt_id(id: UUID,
                            data: EmpruntUpdate,
                            utilisateur: Annotated[User, Depends(get_header_user)],
                            session: Annotated[Session, Depends(get_session)]
) -> Emprunt:
    emprunt = get_emprunt(id, session)
    if not emprunt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="emprunt non trouve")
    if emprunt.user_id != utilisateur.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="vous n'avez pas acces a cet emprunt")
    updated_emprunt = update_emprunt(data, emprunt, session)
    return updated_emprunt

@app_emprunt.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_emprunt_id(id: UUID,
                            utilisateur: Annotated[User, Depends(get_header_user)],
                            session: Annotated[Session, Depends(get_session)]
) -> dict[str,str]:
    emprunt = get_emprunt(id, session)
    if not emprunt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="emprunt non trouve")
    if emprunt.user_id != utilisateur.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="vous n'avez pas acces a cet emprunt")
    delete_emprunt(emprunt, session)
    return {"message":"emprunt supprime"}