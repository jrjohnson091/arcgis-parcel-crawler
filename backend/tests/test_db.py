from datetime import datetime, timezone

import pytest
from app.models import Parcel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

SNAPSHOT_TIME = datetime.now(timezone.utc)


def test_attributes_persistence_integrity(db_session):
    """Verify core persistence and unique index constraint."""
    # 1. Insert valid record
    record = Parcel(
        pid="3970500692", objectid=101, owner1="John Doe", snapshot_at=SNAPSHOT_TIME
    )
    db_session.add(record)
    db_session.commit()

    # 2. Verify retrieval
    stmt = select(Parcel).where(Parcel.pid == "3970500692")
    retrieved = db_session.scalar(stmt)
    assert retrieved.owner1 == "John Doe"
    assert retrieved.snapshot_at == SNAPSHOT_TIME


def test_unique_constraint_enforcement(db_session):
    """Verify that the database rejects duplicate PIDs."""
    # Insert first
    db_session.add(Parcel(pid="202", objectid=101, snapshot_at=SNAPSHOT_TIME))
    db_session.commit()

    # Insert duplicate
    db_session.add(Parcel(pid="202", objectid=101, snapshot_at=SNAPSHOT_TIME))

    # Assert DB raises integrity error
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_nullable_fields_persistence(db_session):
    """Verify that optional fields are stored as NULL when not provided."""
    record = Parcel(pid="3970500692", objectid=101, snapshot_at=SNAPSHOT_TIME)
    db_session.add(record)
    db_session.commit()

    db_session.refresh(record)
    assert record.owner1 is None
    assert record.sale_price is None

def test_geometry_fields_persistence(db_session):
    geometry = {
        "rings": [
            [
                [0.0, 0.0],
                [100.0, 0.0],
                [100.0, 100.0],
                [0.0, 100.0],
                [0.0, 0.0],
            ]
        ]
    }

    record = Parcel(
        pid="3970500693",
        objectid=102,
        snapshot_at=SNAPSHOT_TIME,
        geometry_esri_json=geometry,
        geometry_wkid=2273,
        computed_area_sqft=10_000.0,
        computed_acreage=10_000.0 / 43_560,
        area_computation_method="shapely_single_ring_planar_wkid_2273",
    )

    db_session.add(record)
    db_session.commit()

    retrieved = db_session.scalar(
        select(Parcel).where(Parcel.pid == "3970500693")
    )

    assert retrieved is not None
    assert retrieved.geometry_esri_json == geometry
    assert retrieved.geometry_wkid == 2273
    assert retrieved.computed_area_sqft == 10_000.0
    assert retrieved.computed_acreage == pytest.approx(10_000.0 / 43_560)
    assert retrieved.area_computation_method == "shapely_single_ring_planar_wkid_2273"