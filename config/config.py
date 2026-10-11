from dotenv import load_dotenv
from os import getenv

load_dotenv()

class Config():
    db_url: str | None = getenv("DB_URL")
    secret_key: str | None = getenv("SECRET")