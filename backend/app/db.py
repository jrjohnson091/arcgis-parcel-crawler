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

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

def get_session():
    with Session(engine) as session:
        yield session