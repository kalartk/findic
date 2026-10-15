from sqlmodel import Session, select
from uuid import UUID

from model.models import Avoir

def create_avoir(avoir: Avoir, session: Session):
    try:
        session.add(avoir)
        session.commit()
        session.refresh(avoir)
        return avoir
    except Exception as e:
        session.rollback()
        raise e

def get_avoirs_by_user_id(user_id: int, session: Session) -> list[Avoir]:
    statement = select(Avoir).where(Avoir.user_id == user_id)
    results = session.exec(statement)
    avoirs: list[Avoir] = [res for res in results]
    return avoirs

def get_avoir_by_id(avoir_id: UUID, session: Session) -> Avoir | None:
    statement = select(Avoir).where(Avoir.id == avoir_id)
    results = session.exec(statement)
    avoir: Avoir | None = results.first()
    return avoir

def delete_avoir(data: Avoir, session: Session):
    session.delete(data)
    session.commit()
    return

def update_avoir(avoir: Avoir, data, session: Session) -> Avoir:
    modification = data.model_dump(exclude_unset=True)
    avoir.sqlmodel_update((modification))
    session.add(avoir)
    session.commit()
    session.refresh(avoir)
    return avoir