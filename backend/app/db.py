from sqlmodel import Session, create_engine
from .config import settings
from pydantic import PostgresDsn

db_url = PostgresDsn.build(
    scheme="postgresql",
    username="myuser",
    password="mypassword",
    host="localhost",
    port=5432,
    path="mydatabase",
)

engine = create_engine(settings.)