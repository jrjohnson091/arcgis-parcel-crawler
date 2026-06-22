# Esri represents multipart polygon features as multiple rings under
# geometryType="esriGeometryPolygon". For Charleston parcel data observed so far,
# multi-ring features appear to be disjoint parcel parts, so we sum ring areas.

from typing import Any

from shapely.geometry import Polygon

SQFT_PER_ACRE = 43_560
EXPECTED_WKID = 2273
AREA_COMPUTATION_METHOD = "shapely_planar_wkid_2273"


def compute_area_sqft_from_esri_polygon(geometry: dict[str, Any]) -> float:
    rings = geometry["rings"]

    if not rings:
        raise ValueError("Polygon has no rings")

    polygons = [Polygon(ring) for ring in rings]

    for polygon in polygons:
        if polygon.is_empty:
            raise ValueError("Polygon is empty")
        if not polygon.is_valid:
            raise ValueError("Polygon is invalid")

    return float(sum(polygon.area for polygon in polygons))


def compute_acreage_from_esri_polygon(geometry: dict[str, Any]) -> float:
    return compute_area_sqft_from_esri_polygon(geometry) / SQFT_PER_ACRE
