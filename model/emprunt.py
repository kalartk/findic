from sqlmodel import Session, select
from uuid import UUID

from model.models import Emprunt


def create_emprunt(data: Emprunt, session: Session) -> None:
    try:
        session.add(data)
        session.commit()
    finally:
        session.close()

def get_emprunt(id: UUID, session: Session) -> Emprunt | None:
    try:
        data = session.get(Emprunt, id)
        return data
    finally:
        session.close()

def get_all_emprunt(id: int, session: Session) -> list[Emprunt]:
    try:
        stmt = select(Emprunt).where(Emprunt.user_id == id)
        data = session.exec(stmt).all()
        emprunt_list: list[Emprunt] = []

        for emprunt in data:
            emprunt_list.append(emprunt)

        return emprunt_list
    finally:
        session.close()

def update_emprunt(data_modif, data: Emprunt, session: Session) -> Emprunt:
    try:
        modifcation = data_modif.model_dump(exclude_unset=True)
        data.sqlmodel_update(modifcation)
        session.add(data)
        session.commit()
        return data
    finally:
        session.close()

def delete_emprunt(data: Emprunt, session: Session):
    try:
        session.delete(data)
        session.commit()
        return
    finally:
        session.close()



