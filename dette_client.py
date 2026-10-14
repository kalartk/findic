from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from sqlmodel import Session
from typing import Annotated

from model.models import Dette
from model.models import User
from utils.jwt_func import get_header_user
from database.db import get_session
from model.dette import get_all_dette, create_dette
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



@app_dette.get("/", status_code=status.HTTP_200_OK)
async def get_all_dette_handler(session: Annotated[Session, Depends(get_session)], 
                        utilisateur: Annotated[User, Depends(get_header_user)]
                        ) -> list[Dette]:
    donnees = get_all_dette(utilisateur.id, session)

    return donnees
