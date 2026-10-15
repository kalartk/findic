from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from sqlmodel import Session
from typing import Annotated
from uuid import UUID

from model.models import Dette
from model.models import User
from utils.jwt_func import get_header_user
from database.db import get_session
from model.dette import get_all_dette, create_dette, get_dette_id, update_dette, delete_dette
from model.devise import Devise


app_dette = APIRouter(
    tags=['dette'],
    prefix="/dette"
)

class DetteClient(BaseModel):
    motif: str
    devise: Devise
    montant: float
    proprio: str | None


class DetteClientModif(BaseModel):
    motif: str | None
    devise: Devise | None
    montant: float | None
    proprio: str | None

#Handler pour creer une dette
@app_dette.post("/", status_code=status.HTTP_201_CREATED)
async def create_a_dette(data: DetteClient,
                        session: Annotated[Session, Depends(get_session)], 
                        utilisateur: Annotated[User, Depends(get_header_user)]
                        ) -> dict[str, str]:
    
    create_dette(Dette(
        montant=data.montant,
        motif=data.motif,
        devise=data.devise,
        proprio=data.proprio,
        user_id=utilisateur.id
    ), session)

    return {"message":"dette créer"}


#Handler pour avoir la liste de toute les dettes
@app_dette.get("/", status_code=status.HTTP_200_OK)
async def get_all_dette_handler(session: Annotated[Session, Depends(get_session)], 
                        utilisateur: Annotated[User, Depends(get_header_user)]
                        ) -> list[Dette]:
    donnees = get_all_dette(utilisateur.id, session)

    return donnees

#Handler pour avoir une dette particuliere
@app_dette.get("/{id}", status_code=status.HTTP_200_OK)
async def get_a_dette_id(id:UUID,
                         session: Annotated[Session, Depends(get_session)],
                         utilisateur: Annotated[User, Depends(get_header_user)]) -> Dette:
    data = get_dette_id(id, session)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dette non trouvé")
    if data.user_id != utilisateur.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="operation pas permise")
    return data

#Handler pour modifier les attributs d'une dette
@app_dette.patch("/{id}", status_code=status.HTTP_200_OK)
async def update_dette_infos(id:UUID,
                             data_client: DetteClientModif,
                            session: Annotated[Session, Depends(get_session)],
                            utilisateur: Annotated[User, Depends(get_header_user)]
                            ) -> Dette:
    if data_client.model_dump(exclude_none=True) == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="the new field are required")
    data = get_dette_id(id, session)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dette non trouvé")
    if data.user_id != utilisateur.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="operation non permise")
    new_dette = update_dette(data_client, data, session)

    return new_dette


@app_dette.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_a_dette(id:UUID,
                         session: Annotated[Session, Depends(get_session)],
                         utilisateur: Annotated[User, Depends(get_header_user)]
                                                ) -> dict[str, str]:
    data = get_dette_id(id, session)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dette introuvable")
    
    if data.user_id != utilisateur.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="operation non permise")

    delete_dette(data, session)
    return {"message":"dette effacer"}
    
