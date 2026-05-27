import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

# Use an in-memory SQLite for blazing fast tests, 
# or your local Postgres connection string
DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture
def db_session():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine) # Create tables
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    
    yield session  # The test runs here
    
    session.close()
    Base.metadata.drop_all(engine) # Clean up