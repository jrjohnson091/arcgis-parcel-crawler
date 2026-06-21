from datetime import datetime, timezone
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator, model_validator
from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

MIN_VALID_ARCGIS_DATE = datetime(1800, 1, 1, tzinfo=timezone.utc)
now = datetime.now(timezone.utc)
MAX_VALID_ARCGIS_DATE = now.replace(year=now.year + 1)


class BaseParams(BaseModel):
    where: str = "1=1"
    f: str = "json"


class ParcelFetchParams(BaseParams):
    outFields: str = "*"
    returnGeometry: bool = True
    resultOffset: int = 0
    resultRecordCount: int = 1000
    returnCountOnly: bool = False
    outSR: int = 2273


class ParcelCountParams(BaseParams):
    returnCountOnly: bool = True


class NearbyParcelParams(BaseParams):
    geometryType: str = "esriGeometryPoint"
    inSR: int = 4326
    spatialRel: str = "esriSpatialRelIntersects"
    units: str = "esriSRUnit_StatuteMile"

    lon: float
    lat: float
    distance: float

    @property
    def geometry(self) -> str:
        return f"{self.lon},{self.lat}"

    def to_query_params(self) -> dict[str, Any]:
        data = self.model_dump(exclude={"lon", "lat"})
        data["geometry"] = self.geometry
        return data


class NearbyParcelCountParams(NearbyParcelParams):
    returnCountOnly: bool = True


class NearbyParcelIdsParams(NearbyParcelParams):
    returnIdsOnly: bool = True


class PidLookupParams(BaseParams):
    object_ids: list[int]
    outFields: str = "PID"
    returnGeometry: bool = False

    def to_query_params(self) -> dict[str, Any]:
        data = self.model_dump(exclude={"object_ids"})

        data["objectIds"] = ",".join(str(object_id) for object_id in self.object_ids)

        return data


class RecordsOnlyResponse(BaseModel):
    count: int


class Base(DeclarativeBase):
    """The central structural base class for SQLAlchemy 2.0 tables."""

    pass


class Parcel(Base):
    """Your actual PostgreSQL table structure.

    Expects clean, native Python types.
    """

    __tablename__ = "parcels"

    pid: Mapped[str] = mapped_column(String(15), primary_key=True)

    # Explicit column types combined with PEP-584 type hint mappings
    objectid: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    snapshot_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    owner1: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    owner2: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    tax_district: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    class_code: Mapped[Optional[str]] = mapped_column(
        String(255), index=True, nullable=True
    )
    mail_st_no: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    mail_st_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    mail_st_type: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    mail_2nd_addr: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    mail_2nd_addt: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    mail_city: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    mail_state: Mapped[Optional[str]] = mapped_column(
        String(255), index=True, nullable=True
    )
    mail_zip: Mapped[Optional[str]] = mapped_column(
        String(255), index=True, nullable=True
    )
    mail_country: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    legal_descr: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    subdivision: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    deeded_acreage: Mapped[Optional[float]] = mapped_column(
        Float, index=True, nullable=True
    )
    legal_residence: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    other: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    agr: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    deed_book_page: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    plat_book_page: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    sale_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Pristine native timezone-naive destinations for Postgres TIMESTAMP WITHOUT TIME ZONE
    recorded_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    doc_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    geometry_esri_json: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSONB, nullable=True
    )
    geometry_wkid: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    computed_area_sqft: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    computed_acreage: Mapped[Optional[float]] = mapped_column(
        Float, index=True, nullable=True
    )
    area_computation_method: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True
    )


class ArcGISParcelAttributes(BaseModel):
    """Its only job is to consume, clean, and validate raw API JSON."""

    # Map the nasty uppercase API dot-notation keys directly to clean snake_case properties
    objectid: int = Field(alias="OBJECTID")
    pid: Optional[str] = Field(default=None, alias="PID")
    owner1: Optional[str] = Field(default=None, alias="OWNER1")
    owner2: Optional[str] = Field(default=None, alias="OWNER2")
    tax_district: Optional[str] = Field(default=None, alias="TAX_DISTRICT")
    class_code: Optional[str] = Field(default=None, alias="CLASS_CODE")
    mail_st_no: Optional[str] = Field(default=None, alias="MAIL_ST_NO")
    mail_st_name: Optional[str] = Field(default=None, alias="MAIL_ST_NAME")
    mail_st_type: Optional[str] = Field(default=None, alias="MAIL_ST_TYPE")
    mail_2nd_addr: Optional[str] = Field(default=None, alias="MAIL_2ND_ADDR")
    mail_2nd_addt: Optional[str] = Field(default=None, alias="MAIL_2ND_ADDT")
    mail_city: Optional[str] = Field(default=None, alias="MAIL_CITY")
    mail_state: Optional[str] = Field(default=None, alias="MAIL_STATE")
    mail_zip: Optional[str] = Field(default=None, alias="MAIL_ZIP")
    mail_country: Optional[str] = Field(default=None, alias="MAIL_COUNTRY")
    legal_descr: Optional[str] = Field(default=None, alias="LEGAL_DESCR")
    subdivision: Optional[str] = Field(default=None, alias="SUBDIVISION")
    deeded_acreage: Optional[float] = Field(default=None, alias="ACREAGE")
    legal_residence: Optional[str] = Field(default=None, alias="LEGAL_RESIDENCE")
    other: Optional[str] = Field(default=None, alias="OTHER")
    agr: Optional[str] = Field(default=None, alias="AGR")
    deed_book_page: Optional[str] = Field(default=None, alias="DEED_BOOK_PAGE")
    plat_book_page: Optional[str] = Field(default=None, alias="PLAT_BOOK_PAGE")
    sale_price: Optional[float] = Field(default=None, alias="SALE_PRICE")
    recorded_date: Optional[datetime] = Field(default=None, alias="RECORDED_DATE")
    doc_date: Optional[datetime] = Field(default=None, alias="DOC_DATE")

    @field_validator("recorded_date", "doc_date", mode="before")
    @classmethod
    def transform_ms_to_datetime(cls, value: Any) -> Any:
        if value is None:
            return None

        if isinstance(value, (int, float)) and abs(value) > 1e11:
            parsed_date = datetime.fromtimestamp(value / 1000, tz=timezone.utc)

            if (
                parsed_date < MIN_VALID_ARCGIS_DATE
                or parsed_date > MAX_VALID_ARCGIS_DATE
            ):
                return None

            return parsed_date

        return value

    # Hook 2: Walk the incoming fields, strip whitespace, map empty/blank inputs to None
    @model_validator(mode="before")
    @classmethod
    def strip_all_string_spaces(cls, data: Any) -> Any:
        if isinstance(data, dict):
            cleaned_data = {}
            for key, value in data.items():
                if isinstance(value, str):
                    stripped = value.strip()
                    cleaned_data[key] = stripped if stripped != "" else None
                else:
                    cleaned_data[key] = value
            return cleaned_data
        return data


class EsriPolygonGeometry(BaseModel):
    rings: list[list[list[float]]]


class ArcGISSpatialReference(BaseModel):
    wkid: int | None = None
    latestWkid: int | None = None


class ArcGISParcelFeature(BaseModel):
    attributes: ArcGISParcelAttributes
    geometry: EsriPolygonGeometry | None = None


class ArcGISResponse(BaseModel):
    spatialReference: ArcGISSpatialReference | None = None
    features: list[ArcGISParcelFeature]
    exceededTransferLimit: bool = False


class ArcGISApiError(BaseModel):
    code: int
    message: str
    details: list[Any] = Field(default_factory=list)


class ArcGISErrorResponse(BaseModel):
    error: ArcGISApiError


class ObjectIdsOnlyResponse(BaseModel):
    objectIdFieldName: str
    objectIds: list[int]


class PidOnlySchema(BaseModel):
    pid: str = Field(alias="PID")


class PidOnlyFeature(BaseModel):
    attributes: PidOnlySchema
    geometry: Optional[dict[str, Any]] = None


class PidOnlyResponse(BaseModel):
    features: list[PidOnlyFeature]
