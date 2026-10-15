from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from pydantic import BaseModel
from typing import Annotated
from uuid import UUID

from model.models import User
from model.devise import Devise
from model.models import Avoir
from database.db import get_session
from utils.jwt_func import get_header_user
from model.avoir import create_avoir, get_avoirs_by_user_id, get_avoir_by_id, delete_avoir, update_avoir

app_avoir = APIRouter(prefix="/avoir", tags=["Avoir"])

class AvoirCreate(BaseModel):
    devise: Devise
    montant: float
    proprio: str

class AvoirUpdate(BaseModel):
    devise: Devise | None = None
    montant: float | None = None
    proprio: str | None = None
    statut: bool | None = None

@app_avoir.post("/create", status_code=status.HTTP_201_CREATED)
def create_avoir_endpoint(data: AvoirCreate,
    utilisateur: Annotated[User, Depends(get_header_user)],
    session: Annotated[Session, Depends(get_session)],
) -> dict[str, str]:
    avoir = Avoir(
        devise=data.devise,
        montant=data.montant,
        proprio=data.proprio,
        user_id=utilisateur.id
    )
    create_avoir(avoir, session)
    return {"message": "Avoir créé avec succès"}

@app_avoir.get("/user/all", status_code=status.HTTP_200_OK)
def get_avoirs_handler(
    utilisateur: Annotated[User, Depends(get_header_user)],
    session: Annotated[Session, Depends(get_session)],
):
    return get_avoirs_by_user_id(utilisateur.id, session)

@app_avoir.get("/{id:uuid}", status_code=status.HTTP_200_OK)
def get_avoir_by_id_handler(
    id: UUID,
    utilisateur: Annotated[User, Depends(get_header_user)],
    session: Annotated[Session, Depends(get_session)],
):
    avoir = get_avoir_by_id(id, session)
    if not avoir:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Avoir non trouvé")
    if avoir.user_id != utilisateur.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")
    return avoir

@app_avoir.put("/{id:uuid}", status_code=status.HTTP_200_OK)
def update_avoir_handler(
    id: UUID,
    data: AvoirUpdate,
    utilisateur: Annotated[User, Depends(get_header_user)],
    session: Annotated[Session, Depends(get_session)],
):
    if data.model_dump(exclude_unset=True) == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Aucune donnée à mettre à jour")
    avoir = get_avoir_by_id(id, session)
    if not avoir:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Avoir non trouvé")
    if avoir.user_id != utilisateur.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")
    updated_avoir = update_avoir(avoir, data, session)
    return updated_avoir

@app_avoir.delete("/{id:uuid}", status_code=status.HTTP_200_OK)
def delete_avoir_handler(
    id: UUID,
    utilisateur: Annotated[User, Depends(get_header_user)],
    session: Annotated[Session, Depends(get_session)],
):
    avoir = get_avoir_by_id(id, session)
    if not avoir:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Avoir non trouvé")
    if avoir.user_id != utilisateur.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")
    delete_avoir(avoir, session)
    return {"message": "Avoir supprimé avec succès"}
