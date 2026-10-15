from model.models import Dette
from sqlmodel import Session, select
from uuid import UUID

#Creer une dette
def create_dette(data: Dette, session: Session):
    try:
        session.add(data)
        session.commit()
        return
    
    finally:
        session.close

#chercher une dette
def get_dette_id(id: UUID, session: Session) -> Dette | None:
    try:
        data = session.exec(select(Dette).where(Dette.id == id)).first()
        return data
    finally:
        session.close()

#get all dettes in the db
def get_all_dette(id: int, session: Session) -> list[Dette]:
    try:
        stmt = select(Dette).where(Dette.user_id == id)
        rows = session.exec(stmt).all()
        data: list[Dette] = []
        for row in rows:
            data.append(row)

        return data
    finally:
        session.close()

def update_dette(data_modif, donne_dette: Dette, session: Session) -> Dette:
    try:
        modifications = data_modif.model_dump(exclude_unset=True)
        donne_dette.sqlmodel_update(modifications)
        session.add(donne_dette)
        session.commit()
        session.refresh(donne_dette)

        return donne_dette

    finally:
        session.close()


def delete_dette(data: Dette, session: Session) -> None:
    try:
        session.delete(data)
        session.commit()
        return
    finally:
        session.close()

