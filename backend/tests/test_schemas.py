from datetime import datetime, timezone
import pytest
from pydantic import ValidationError

# Make sure this import accurately points to where your pure Pydantic schemas live
from app.models import ArcGISResponse


@pytest.fixture
def raw_charleston_county_json():
    """Fixture providing a realistic, comprehensive mock payload from the live server."""
    return {
        "displayFieldName": "FEATURES.SDE.P_POLY_PARCEL.PID",
        "fieldAliases": {
            "FEATURES.SDE.P_POLY_PARCEL.OBJECTID": "OBJECTID",
            "FEATURES.SDE.P_POLY_PARCEL.PID": "PID",
            "FEATURES.SDE.P_POLY_PARCEL.GPIN": "GPIN",
            "FEATURES.SDE.P_POLY_PARCEL.ACRES_CAL": "Calculated Acres",
            "FEATURES.SDE.CAMA.OWNER1": "OWNER1",
            "FEATURES.SDE.CAMA.OWNER2": "OWNER2",
            "FEATURES.SDE.CAMA.TAX_DISTRICT": "TAX DISTRICT",
            "FEATURES.SDE.CAMA.CLASS_CODE": "CLASS CODE",
            "FEATURES.SDE.CAMA.MAIL_ST_NO": "MAIL_ST_NO",
            "FEATURES.SDE.CAMA.MAIL_ST_NAME": "MAIL_ST_NAME",
            "FEATURES.SDE.CAMA.MAIL_ST_TYPE": "MAIL_ST_TYPE",
            "FEATURES.SDE.CAMA.MAIL_2ND_ADDR": "MAIL_2ND_ADDR",
            "FEATURES.SDE.CAMA.MAIL_2ND_ADDT": "MAIL_2ND_ADDT",
            "FEATURES.SDE.CAMA.MAIL_CITY": "MAIL_CITY",
            "FEATURES.SDE.CAMA.MAIL_STATE": "MAIL_STATE",
            "FEATURES.SDE.CAMA.MAIL_ZIP": "MAIL_ZIP",
            "FEATURES.SDE.CAMA.MAIL_COUNTRY": "MAIL_COUNTRY",
            "FEATURES.SDE.CAMA.LEGAL_DESCR": "LEGAL DESCRIPTION",
            "FEATURES.SDE.CAMA.SUBDIVISION": "SUBDIVISION",
            "FEATURES.SDE.CAMA.ACREAGE": "DEEDED ACREAGE",
            "FEATURES.SDE.CAMA.LEGAL_RESIDENCE": "LEGAL RESIDENCE",
            "FEATURES.SDE.CAMA.OTHER": "OTHER",
            "FEATURES.SDE.CAMA.AGR": "AGR",
            "FEATURES.SDE.CAMA.DEED_BOOK_PAGE": "DEED BOOK PAGE",
            "FEATURES.SDE.CAMA.PLAT_BOOK_PAGE": "PLAT BOOK PAGE",
            "FEATURES.SDE.CAMA.SALE_PRICE": "SALE_PRICE",
            "FEATURES.SDE.CAMA.RECORDED_DATE": "RECORDED_DATE",
            "FEATURES.SDE.CAMA.DOC_DATE": "DOC_DATE",
        },
        "geometryType": "esriGeometryPolygon",
        "spatialReference": {"wkid": 2273, "latestWkid": 2273},
        "fields": [
            {
                "name": "FEATURES.SDE.P_POLY_PARCEL.OBJECTID",
                "type": "esriFieldTypeOID",
                "alias": "OBJECTID",
            },
            {
                "name": "FEATURES.SDE.P_POLY_PARCEL.PID",
                "type": "esriFieldTypeString",
                "alias": "PID",
                "length": 15,
            },
            {
                "name": "FEATURES.SDE.P_POLY_PARCEL.GPIN",
                "type": "esriFieldTypeString",
                "alias": "GPIN",
                "length": 16,
            },
            {
                "name": "FEATURES.SDE.P_POLY_PARCEL.ACRES_CAL",
                "type": "esriFieldTypeDouble",
                "alias": "Calculated Acres",
            },
            {
                "name": "FEATURES.SDE.CAMA.OWNER1",
                "type": "esriFieldTypeString",
                "alias": "OWNER1",
                "length": 255,
            },
            {
                "name": "FEATURES.SDE.CAMA.OWNER2",
                "type": "esriFieldTypeString",
                "alias": "OWNER2",
                "length": 255,
            },
            {
                "name": "FEATURES.SDE.CAMA.TAX_DISTRICT",
                "type": "esriFieldTypeString",
                "alias": "TAX DISTRICT",
                "length": 255,
            },
            {
                "name": "FEATURES.SDE.CAMA.CLASS_CODE",
                "type": "esriFieldTypeString",
                "alias": "CLASS CODE",
                "length": 255,
            },
            {
                "name": "FEATURES.SDE.CAMA.MAIL_ST_NO",
                "type": "esriFieldTypeString",
                "alias": "MAIL_ST_NO",
                "length": 255,
            },
            {
                "name": "FEATURES.SDE.CAMA.MAIL_ST_NAME",
                "type": "esriFieldTypeString",
                "alias": "MAIL_ST_NAME",
                "length": 255,
            },
            {
                "name": "FEATURES.SDE.CAMA.MAIL_ST_TYPE",
                "type": "esriFieldTypeString",
                "alias": "MAIL_ST_TYPE",
                "length": 255,
            },
            {
                "name": "FEATURES.SDE.CAMA.MAIL_2ND_ADDR",
                "type": "esriFieldTypeString",
                "alias": "MAIL_2ND_ADDR",
                "length": 255,
            },
            {
                "name": "FEATURES.SDE.CAMA.MAIL_2ND_ADDT",
                "type": "esriFieldTypeString",
                "alias": "MAIL_2ND_ADDT",
                "length": 255,
            },
            {
                "name": "FEATURES.SDE.CAMA.MAIL_CITY",
                "type": "esriFieldTypeString",
                "alias": "MAIL_CITY",
                "length": 255,
            },
            {
                "name": "FEATURES.SDE.CAMA.MAIL_STATE",
                "type": "esriFieldTypeString",
                "alias": "MAIL_STATE",
                "length": 255,
            },
            {
                "name": "FEATURES.SDE.CAMA.MAIL_ZIP",
                "type": "esriFieldTypeString",
                "alias": "MAIL_ZIP",
                "length": 255,
            },
            {
                "name": "FEATURES.SDE.CAMA.MAIL_COUNTRY",
                "type": "esriFieldTypeString",
                "alias": "MAIL_COUNTRY",
                "length": 255,
            },
            {
                "name": "FEATURES.SDE.CAMA.LEGAL_DESCR",
                "type": "esriFieldTypeString",
                "alias": "LEGAL DESCRIPTION",
                "length": 255,
            },
            {
                "name": "FEATURES.SDE.CAMA.SUBDIVISION",
                "type": "esriFieldTypeString",
                "alias": "SUBDIVISION",
                "length": 255,
            },
            {
                "name": "FEATURES.SDE.CAMA.ACREAGE",
                "type": "esriFieldTypeDouble",
                "alias": "DEEDED ACREAGE",
            },
            {
                "name": "FEATURES.SDE.CAMA.LEGAL_RESIDENCE",
                "type": "esriFieldTypeString",
                "alias": "LEGAL RESIDENCE",
                "length": 255,
            },
            {
                "name": "FEATURES.SDE.CAMA.OTHER",
                "type": "esriFieldTypeString",
                "alias": "OTHER",
                "length": 255,
            },
            {
                "name": "FEATURES.SDE.CAMA.AGR",
                "type": "esriFieldTypeString",
                "alias": "AGR",
                "length": 255,
            },
            {
                "name": "FEATURES.SDE.CAMA.DEED_BOOK_PAGE",
                "type": "esriFieldTypeString",
                "alias": "DEED BOOK PAGE",
                "length": 255,
            },
            {
                "name": "FEATURES.SDE.CAMA.PLAT_BOOK_PAGE",
                "type": "esriFieldTypeString",
                "alias": "PLAT BOOK PAGE",
                "length": 255,
            },
            {
                "name": "FEATURES.SDE.CAMA.SALE_PRICE",
                "type": "esriFieldTypeDouble",
                "alias": "SALE_PRICE",
            },
            {
                "name": "FEATURES.SDE.CAMA.RECORDED_DATE",
                "type": "esriFieldTypeDate",
                "alias": "RECORDED_DATE",
                "length": 8,
            },
            {
                "name": "FEATURES.SDE.CAMA.DOC_DATE",
                "type": "esriFieldTypeDate",
                "alias": "DOC_DATE",
                "length": 8,
            },
        ],
        "features": [
            {
                "attributes": {
                    "FEATURES.SDE.P_POLY_PARCEL.OBJECTID": 1,
                    "FEATURES.SDE.P_POLY_PARCEL.PID": "0230000028",
                    "FEATURES.SDE.P_POLY_PARCEL.GPIN": " ",
                    "FEATURES.SDE.P_POLY_PARCEL.ACRES_CAL": 2.87261319,
                    "FEATURES.SDE.CAMA.OWNER1": "BYARS WILLIAM CONRAD Jr",
                    "FEATURES.SDE.CAMA.OWNER2": "",
                    "FEATURES.SDE.CAMA.TAX_DISTRICT": "8-1             ",
                    "FEATURES.SDE.CAMA.CLASS_CODE": "905 - VAC-RES-LOT                                               ",
                    "FEATURES.SDE.CAMA.MAIL_ST_NO": "178",
                    "FEATURES.SDE.CAMA.MAIL_ST_NAME": "SHEALY                                                          ",
                    "FEATURES.SDE.CAMA.MAIL_ST_TYPE": "DR      ",
                    "FEATURES.SDE.CAMA.MAIL_2ND_ADDR": "        ",
                    "FEATURES.SDE.CAMA.MAIL_2ND_ADDT": "        ",
                    "FEATURES.SDE.CAMA.MAIL_CITY": "PROSPERITY                      ",
                    "FEATURES.SDE.CAMA.MAIL_STATE": "SC  ",
                    "FEATURES.SDE.CAMA.MAIL_ZIP": "29127           ",
                    "FEATURES.SDE.CAMA.MAIL_COUNTRY": "                                ",
                    "FEATURES.SDE.CAMA.LEGAL_DESCR": "PART LT 28",
                    "FEATURES.SDE.CAMA.SUBDIVISION": " ",
                    "FEATURES.SDE.CAMA.ACREAGE": 2.49,
                    "FEATURES.SDE.CAMA.LEGAL_RESIDENCE": "N",
                    "FEATURES.SDE.CAMA.OTHER": "N",
                    "FEATURES.SDE.CAMA.AGR": "N",
                    "FEATURES.SDE.CAMA.DEED_BOOK_PAGE": "1323-078",
                    "FEATURES.SDE.CAMA.PLAT_BOOK_PAGE": " B-58 ",
                    "FEATURES.SDE.CAMA.SALE_PRICE": 208500.0,
                    "FEATURES.SDE.CAMA.RECORDED_DATE": 1751414400000,
                    "FEATURES.SDE.CAMA.DOC_DATE": 1751241600000,
                },
                "geometry": {
                    "rings": [
                        [
                            [2214102.0557660758, 255385.6252091974],
                            [2213689.9006398916, 255320.85593879223],
                            [2213549.3368730247, 255495.90844611824],
                            [2213764.9040246904, 255705.36765450239],
                            [2214102.0557660758, 255385.6252091974],
                        ]
                    ]
                },
            }
        ],
        "exceededTransferLimit": True,
    }


def test_full_pipeline_deserialization(raw_charleston_county_json):
    """Verifies that root fields are filtered out and child models parse properly."""
    # ACT
    response = ArcGISResponse.model_validate(raw_charleston_county_json)

    # ASSERT
    assert len(response.features) == 1
    feature = response.features[0]

    # Verify Geometry dictionary was carried over untouched
    assert "rings" in feature.geometry
    assert len(feature.geometry["rings"][0]) == 5


def test_alias_mapping_and_primitive_types(raw_charleston_county_json):
    """Ensures raw dot-notation keys accurately map to snake_case attributes."""
    response = ArcGISResponse.model_validate(raw_charleston_county_json)
    attrs = response.features[0].attributes

    assert attrs.features_sde_p_poly_parcel_objectid == 1
    assert attrs.features_sde_p_poly_parcel_acres_cal == 2.87261319
    assert attrs.features_sde_cama_sale_price == 208500.0


def test_string_whitespace_and_empty_space_stripping(raw_charleston_county_json):
    """Ensures blank fields convert to None and text fields strip extra padding."""
    response = ArcGISResponse.model_validate(raw_charleston_county_json)
    attrs = response.features[0].attributes

    # Truncated or clean values
    assert attrs.features_sde_cama_owner1 == "BYARS WILLIAM CONRAD Jr"
    assert attrs.features_sde_cama_tax_district == "8-1"
    assert attrs.features_sde_cama_class_code == "905 - VAC-RES-LOT"
    assert attrs.features_sde_cama_mail_st_name == "SHEALY"
    assert attrs.features_sde_cama_mail_st_type == "DR"
    assert attrs.features_sde_cama_mail_city == "PROSPERITY"
    assert attrs.features_sde_cama_mail_state == "SC"
    assert attrs.features_sde_cama_mail_zip == "29127"
    assert (
        attrs.features_sde_cama_plat_book_page == "B-58"
    )  # Internal spaces kept, padding removed

    # Space strings or empty quotes converted completely to None
    assert attrs.features_sde_p_poly_parcel_gpin is None
    assert attrs.features_sde_cama_owner2 is None
    assert attrs.features_sde_cama_mail_2nd_addr is None
    assert attrs.features_sde_cama_mail_2nd_addt is None
    assert attrs.features_sde_cama_mail_country is None
    assert attrs.features_sde_cama_subdivision is None


def test_epoch_milliseconds_transform_to_utc_datetime(raw_charleston_county_json):
    """Verifies huge bigint timestamps become valid timezone-aware datetimes."""
    response = ArcGISResponse.model_validate(raw_charleston_county_json)
    attrs = response.features[0].attributes

    # Expected Values computed from: value / 1000
    expected_recorded = datetime.fromtimestamp(1751414400, tz=timezone.utc)
    expected_doc = datetime.fromtimestamp(1751241600, tz=timezone.utc)

    assert isinstance(attrs.features_sde_cama_recorded_date, datetime)
    assert attrs.features_sde_cama_recorded_date.tzinfo == timezone.utc
    assert attrs.features_sde_cama_recorded_date == expected_recorded

    assert isinstance(attrs.features_sde_cama_doc_date, datetime)
    assert attrs.features_sde_cama_doc_date.tzinfo == timezone.utc
    assert attrs.features_sde_cama_doc_date == expected_doc


def test_missing_required_id_field_throws_validation_error(raw_charleston_county_json):
    """Ensures missing mandatory identifiers trigger immediate safe extraction failures."""
    # Delete the vital key from the nested dict structure
    del raw_charleston_county_json["features"][0]["attributes"][
        "FEATURES.SDE.P_POLY_PARCEL.OBJECTID"
    ]

    with pytest.raises(ValidationError) as excinfo:
        ArcGISResponse.model_validate(raw_charleston_county_json)

    assert "FEATURES.SDE.P_POLY_PARCEL.OBJECTID" in str(excinfo.value)


def test_handles_multiple_features_in_payload():
    """Verify that multiple features in the 'features' array are processed correctly."""
    multi_record_json = {
        "features": [
            {
                "attributes": {
                    "FEATURES.SDE.P_POLY_PARCEL.OBJECTID": 1,
                    "FEATURES.SDE.P_POLY_PARCEL.PID": "001",
                }
            },
            {
                "attributes": {
                    "FEATURES.SDE.P_POLY_PARCEL.OBJECTID": 2,
                    "FEATURES.SDE.P_POLY_PARCEL.PID": "002",
                }
            },
        ]
    }

    # ACT
    response = ArcGISResponse.model_validate(multi_record_json)

    # ASSERT
    assert len(response.features) == 2
    assert response.features[0].attributes.features_sde_p_poly_parcel_objectid == 1
    assert response.features[1].attributes.features_sde_p_poly_parcel_objectid == 2
