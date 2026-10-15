from sqlmodel import Session, select
from sqlalchemy import update
from uuid import UUID

from model.models import Depense


def create_depense(data: Depense, session:Session):
    try:
        session.add(data)
        session.commit()

    finally:
        session.close

def get_depenses(id: int, session: Session) -> list[Depense] | None:
    try:
        stmt = select(Depense).where(Depense.user_id == id)
        datas = session.exec(statement=stmt).all()
        depenses = []
        for depense in datas:
            depenses.append(depense)
        return depenses
    finally:
        session.close()


def get_depense_id(id:UUID, session: Session) -> Depense | None:
    try:
        data = session.exec(select(Depense).where(Depense.id == id)).first()
        return data
    finally:
        session.close()

def update_depense_id(data, session: Session, depense: Depense) -> Depense:
    try:
        modification = data.model_dump(exclude_unset=True)
        depense.sqlmodel_update((modification))
        session.add(depense)
        session.commit()
        session.refresh(depense)

        return depense
    finally:
        session.close()

def delete_depense_id(data: Depense, session: Session) -> None:
    try:
        session.delete(data)
        session.commit()
        return
    finally:
        session.close()
        