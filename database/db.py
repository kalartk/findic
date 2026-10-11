from sqlmodel import SQLModel, Session, create_engine

from config.config import Config

URL = Config.db_url if Config.db_url else "sqlite:///test.db"

engine = create_engine(url=URL)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        try:
           yield session
        finally:
           session.close()