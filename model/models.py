from sqlmodel import SQLModel, Field
from uuid import UUID, uuid7
from datetime import datetime, timezone

from model.devise import Devise

class UserBase(SQLModel):
    nom: str
    prenom: str
    email: str = Field(unique=True, index=True)
    password: str
    pseudo: str | None = Field(default=None, unique=True, index=True)
    created_at: datetime = Field(default=datetime.now(timezone.utc))

class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)

class DepenseBase(SQLModel):
    motif: str
    devise: Devise
    montant: float
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default=datetime.now(timezone.utc))

class Depense(DepenseBase, table=True):
    id: UUID = Field(default=uuid7(), primary_key=True)

class DetteBase(SQLModel):
    motif: str
    devise: Devise
    montant: float
    proprio: str | None
    statut: bool = Field(default=False)
    user_id: int = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default=datetime.now(timezone.utc))

class Dette(DetteBase, table=True):
    id: UUID = Field(default=uuid7(), primary_key=True)

class EmpruntBase(SQLModel):
    montant: int
    proprio: str
    statut: bool = Field(default=False)
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default=datetime.now(timezone.utc))

class Emprunt(EmpruntBase, table=True):
    id: UUID = Field(default=uuid7(), primary_key=True)

class AvoirBase(SQLModel):
    devise: Devise
    montant: float
    proprio: str
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default=datetime.now(timezone.utc))

class Avoir(AvoirBase, table=True):
    id: UUID = Field(default=uuid7(), primary_key=True)