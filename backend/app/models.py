from datetime import datetime, timezone
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator, model_validator
from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Params(BaseModel):
    where: str = "1=1"
    outFields: str = "*"
    returnGeometry: bool = False
    resultOffset: int = 0
    resultRecordCount: int = 1000
    returnCountOnly: bool = True
    f: str = "json"


class RecordsOnlyResponse(BaseModel):
    count: int


class Base(DeclarativeBase):
    """The central structural base class for SQLAlchemy 2.0 tables."""

    pass


class Attributes(Base):
    """Your actual PostgreSQL table structure.

    Expects clean, native Python types.
    """

    __tablename__ = "parcel_records"

    # Explicit column types combined with PEP-584 type hint mappings
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    objectid: Mapped[int] = mapped_column(Integer, index=True, unique=True)
    pid: Mapped[Optional[str]] = mapped_column(String(15), nullable=True)
    owner1: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    owner2: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    tax_district: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    class_code: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    mail_st_no: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    mail_st_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    mail_st_type: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    mail_2nd_addr: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    mail_2nd_addt: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    mail_city: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    mail_state: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    mail_zip: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    mail_country: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    legal_descr: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    subdivision: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    acreage: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    legal_residence: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    other: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    agr: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    deed_book_page: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    plat_book_page: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    sale_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Pristine native timezone-naive destinations for Postgres TIMESTAMP WITHOUT TIME ZONE
    recorded_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    doc_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class InboundAttributesSchema(BaseModel):
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
    acreage: Optional[float] = Field(default=None, alias="ACREAGE")
    legal_residence: Optional[str] = Field(default=None, alias="LEGAL_RESIDENCE")
    other: Optional[str] = Field(default=None, alias="OTHER")
    agr: Optional[str] = Field(default=None, alias="AGR")
    deed_book_page: Optional[str] = Field(default=None, alias="DEED_BOOK_PAGE")
    plat_book_page: Optional[str] = Field(default=None, alias="PLAT_BOOK_PAGE")
    sale_price: Optional[float] = Field(default=None, alias="SALE_PRICE")
    recorded_date: Optional[datetime] = Field(default=None, alias="RECORDED_DATE")
    doc_date: Optional[datetime] = Field(default=None, alias="DOC_DATE")

    # Hook 1: Automatically transform millisecond bigints to UTC Datetime objects
    @field_validator("recorded_date", "doc_date", mode="before")
    @classmethod
    def transform_ms_to_datetime(cls, value: Any) -> Any:
        if isinstance(value, (int, float)) and value > 1e11:
            return datetime.fromtimestamp(value / 1000, tz=timezone.utc)
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


class Feature(BaseModel):
    attributes: InboundAttributesSchema
    geometry: Optional[dict[str, Any]] = None


class ArcGISResponse(BaseModel):
    features: list[Feature]
    exceededTransferLimit: Optional[bool] = False


class ArcGIS_API_Error(BaseModel):
    code: int
    message: str
    details: list[Any] = []


class ArcGIS_Error_Response(BaseModel):
    error: ArcGIS_API_Error
