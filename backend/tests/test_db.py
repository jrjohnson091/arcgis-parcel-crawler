import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.models import Attributes


def test_attributes_persistence_integrity(db_session):
    """Verify core persistence and unique index constraint."""
    # 1. Insert valid record
    record = Attributes(objectid=101, owner1="John Doe")
    db_session.add(record)
    db_session.commit()

    # 2. Verify retrieval
    stmt = select(Attributes).where(Attributes.objectid == 101)
    retrieved = db_session.scalar(stmt)
    assert retrieved.owner1 == "John Doe"


def test_unique_constraint_enforcement(db_session):
    """Verify that the database rejects duplicate ObjectIDs."""
    # Insert first
    db_session.add(Attributes(objectid=202))
    db_session.commit()

    # Insert duplicate
    db_session.add(Attributes(objectid=202))

    # Assert DB raises integrity error
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_nullable_fields_persistence(db_session):
    """Verify that optional fields are stored as NULL when not provided."""
    record = Attributes(objectid=303)
    db_session.add(record)
    db_session.commit()

    db_session.refresh(record)
    assert record.owner1 is None
    assert record.sale_price is None
