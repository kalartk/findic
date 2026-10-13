from fastapi import APIRouter, status, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session
from typing import Annotated
from uuid import UUID

from model.models import User
from model.models import Depense
from utils.jwt_func import get_header_user
from database.db import get_session
from model.devise import Devise
from model.depense import get_depenses, get_depense_id, update_depense_id, delete_depense_id, create_depense

app_depense = APIRouter()
app_depense.prefix = "/depense"
app_depense.tags = ['depense']

class DepenseClient(BaseModel):
    motif: str
    devise: Devise
    montant: float

@app_depense.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_depense(data: DepenseClient,
                            session: Annotated[Session, Depends(get_session)],
                            utilisateur: Annotated[User, Depends(get_header_user)]
                               ) -> dict[str, str]:

    create_depense(data=Depense(motif=data.motif,
                                devise=data.devise, 
                                montant=data.montant, 
                                user_id=utilisateur.id), 
                            session=session)
    return {"message":f"depense créer"}

@app_depense.get("/all")
async def get_depenses_handler(session: Annotated[Session, Depends(get_session)],
                               utilisateur: Annotated[User, Depends(get_header_user)]
                               ) -> list[Depense] | None:
    donnee = get_depenses(id=utilisateur.id, session=session)
    return donnee

@app_depense.get("/{id}")
async def get_depense_by_id(id: UUID,
                            session: Annotated[Session, Depends(get_session)],
                            utilisateur: Annotated[User, Depends(get_header_user)]
                        ) -> Depense | None:
    donnee = get_depense_id(id=id, session=session)
    if donnee:
        if donnee.user_id != utilisateur.id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='not authorized operation')

    return donnee

@app_depense.patch("/{id}")
async def update_depense(id: UUID,
                         data: DepenseClient,
                            session: Annotated[Session, Depends(get_session)],
                            utilisateur: Annotated[User, Depends(get_header_user)]
                            ) -> Depense:
    donnee = get_depense_id(id=id, session=session)
    if not donnee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no todo whith that id sorry")
    if donnee.user_id != utilisateur.id:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="operation pas permise")

    donne_retur = update_depense_id(id=id, data=data, session=session, depense=donnee)
    return donne_retur

@app_depense.delete("/{id}")
async def delete_depense(id: UUID, 
                         session: Annotated[Session, Depends(get_session)],
                         utilisateur: Annotated[User, Depends(get_header_user)]
                         ) -> dict[str, str]:
    donnee = get_depense_id(id=id, session=session)
    if not donnee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="depense introuvable")

    if donnee.user_id != utilisateur.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="operation pas permise")

    delete_depense_id(donnee, session)
    return {"message":"depense supprimer"}


    