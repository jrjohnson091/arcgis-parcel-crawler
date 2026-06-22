import pytest
from app.geometry import (
    compute_acreage_from_esri_polygon,
    compute_area_sqft_from_esri_polygon,
)


def test_compute_area_for_100_by_100_square():
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

    assert compute_area_sqft_from_esri_polygon(geometry) == 10_000.0


def test_compute_acreage_from_single_ring_square():
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

    assert compute_acreage_from_esri_polygon(geometry) == pytest.approx(10_000 / 43_560)


def test_no_rings_raise_error():
    geometry = {"rings": []}

    with pytest.raises(ValueError, match="Polygon has no rings"):
        compute_area_sqft_from_esri_polygon(geometry)


def test_compute_area_sqft_from_multiple_disjoint_rings():
    geometry = {
        "rings": [
            [[0, 0], [100, 0], [100, 100], [0, 100], [0, 0]],
            [[200, 0], [300, 0], [300, 100], [200, 100], [200, 0]],
        ]
    }

    assert compute_area_sqft_from_esri_polygon(geometry) == pytest.approx(20_000)
