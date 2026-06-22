import pytest
from app.config import settings
from app.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture
def db_session():
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    Base.metadata.create_all(engine) # Create tables
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    
    yield session  # The test runs here
    
    session.close()
    Base.metadata.drop_all(engine) # Clean up