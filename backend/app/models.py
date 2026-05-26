from datetime import datetime, timezone
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, field_validator, model_validator
from sqlmodel import Field, SQLModel

# params = {
#     # "where": "1=1",
#     # "where": "FEATURES.SDE_CAMA.OWNER1 LIKE 'JOHNSON%JOSHUA%'",
#     "where": "FEATURES.SDE.CAMA.OWNER1 LIKE 'MURRAY%MATT%'",
#     "outFields": "*",
#     "returnGeometry": "false",
#     "f": "json",
#     # "returnCountOnly": "true"
#     # "resultOffset": 0,
#     # "resultRecordCount": 1, # 1000,
# }


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


class Attributes(SQLModel, table=True):
    __tablename__ = "parcel_records"
    
    # Unified configuration to handle dot-notation API mapping inputs
    model_config = ConfigDict(populate_by_name=True)

    # 1. Primary engine sequence key for relational tracking in Postgres
    id: Optional[int] = Field(default=None, primary_key=True)

    # 2. Native database column layout mappings matching your Pydantic properties
    features_sde_p_poly_parcel_objectid: int = Field(
        index=True, unique=True, alias="FEATURES.SDE.P_POLY_PARCEL.OBJECTID"
    )
    features_sde_p_poly_parcel_pid: Optional[str] = Field(
        default=None, max_length=15, alias="FEATURES.SDE.P_POLY_PARCEL.PID"
    )
    features_sde_p_poly_parcel_gpin: Optional[str] = Field(
        default=None, max_length=16, alias="FEATURES.SDE.P_POLY_PARCEL.GPIN"
    )
    features_sde_p_poly_parcel_acres_cal: Optional[float] = Field(
        default=None, alias="FEATURES.SDE.P_POLY_PARCEL.ACRES_CAL"
    )
    features_sde_cama_owner1: Optional[str] = Field(
        default=None, max_length=255, alias="FEATURES.SDE.CAMA.OWNER1"
    )
    features_sde_cama_owner2: Optional[str] = Field(
        default=None, max_length=255, alias="FEATURES.SDE.CAMA.OWNER2"
    )
    features_sde_cama_tax_district: Optional[str] = Field(
        default=None, max_length=255, alias="FEATURES.SDE.CAMA.TAX_DISTRICT"
    )
    features_sde_cama_class_code: Optional[str] = Field(
        default=None, max_length=255, alias="FEATURES.SDE.CAMA.CLASS_CODE"
    )
    features_sde_cama_mail_st_no: Optional[str] = Field(
        default=None, max_length=255, alias="FEATURES.SDE.CAMA.MAIL_ST_NO"
    )
    features_sde_cama_mail_st_name: Optional[str] = Field(
        default=None, max_length=255, alias="FEATURES.SDE.CAMA.MAIL_ST_NAME"
    )
    features_sde_cama_mail_st_type: Optional[str] = Field(
        default=None, max_length=255, alias="FEATURES.SDE.CAMA.MAIL_ST_TYPE"
    )
    features_sde_cama_mail_2nd_addr: Optional[str] = Field(
        default=None, max_length=255, alias="FEATURES.SDE.CAMA.MAIL_2ND_ADDR"
    )
    features_sde_cama_mail_2nd_addt: Optional[str] = Field(
        default=None, max_length=255, alias="FEATURES.SDE.CAMA.MAIL_2ND_ADDT"
    )
    features_sde_cama_mail_city: Optional[str] = Field(
        default=None, max_length=255, alias="FEATURES.SDE.CAMA.MAIL_CITY"
    )
    features_sde_cama_mail_state: Optional[str] = Field(
        default=None, max_length=255, alias="FEATURES.SDE.CAMA.MAIL_STATE"
    )
    features_sde_cama_mail_zip: Optional[str] = Field(
        default=None, max_length=255, alias="FEATURES.SDE.CAMA.MAIL_ZIP"
    )
    features_sde_cama_mail_country: Optional[str] = Field(
        default=None, max_length=255, alias="FEATURES.SDE.CAMA.MAIL_COUNTRY"
    )
    features_sde_cama_legal_descr: Optional[str] = Field(
        default=None, max_length=255, alias="FEATURES.SDE.CAMA.LEGAL_DESCR"
    )
    features_sde_cama_subdivision: Optional[str] = Field(
        default=None, max_length=255, alias="FEATURES.SDE.CAMA.SUBDIVISION"
    )
    features_sde_cama_acreage: Optional[float] = Field(
        default=None, alias="FEATURES.SDE.CAMA.ACREAGE"
    )
    features_sde_cama_legal_residence: Optional[str] = Field(
        default=None, max_length=255, alias="FEATURES.SDE.CAMA.LEGAL_RESIDENCE"
    )
    features_sde_cama_other: Optional[str] = Field(
        default=None, max_length=255, alias="FEATURES.SDE.CAMA.OTHER"
    )
    features_sde_cama_agr: Optional[str] = Field(
        default=None, max_length=255, alias="FEATURES.SDE.CAMA.AGR"
    )
    features_sde_cama_deed_book_page: Optional[str] = Field(
        default=None, max_length=255, alias="FEATURES.SDE.CAMA.DEED_BOOK_PAGE"
    )
    features_sde_cama_plat_book_page: Optional[str] = Field(
        default=None, max_length=255, alias="FEATURES.SDE.CAMA.PLAT_BOOK_PAGE"
    )
    features_sde_cama_sale_price: Optional[float] = Field(
        default=None, alias="FEATURES.SDE.CAMA.SALE_PRICE"
    )
    features_sde_cama_recorded_date: Optional[datetime] = Field(
        default=None, alias="FEATURES.SDE.CAMA.RECORDED_DATE"
    )
    features_sde_cama_doc_date: Optional[datetime] = Field(
        default=None, alias="FEATURES.SDE.CAMA.DOC_DATE"
    )

    # 3. Intercept millisecond database epochs from ArcGIS
    @field_validator(
        "features_sde_cama_recorded_date", "features_sde_cama_doc_date", mode="before"
    )
    @classmethod
    def transform_ms_to_datetime(cls, value: Any) -> Any:
        if isinstance(value, (int, float)) and value > 1e11:
            return datetime.fromtimestamp(value / 1000, tz=timezone.utc)
        return value
    
    # 4. Global string stripping execution boundary
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
    attributes: Attributes
    geometry: Optional[dict[str, Any]] = None


class ArcGISResponse(BaseModel):
    features: list[Feature]


class ArcGIS_API_Error(BaseModel):
    code: int
    message: str
    details: list[Any] = []


class ArcGIS_Error_Response(BaseModel):
    error: ArcGIS_API_Error
