from datetime import datetime, timezone
import pytest
from pydantic import ValidationError

# Make sure this import accurately points to where your pure Pydantic schemas live
from app.models import ArcGISResponse


@pytest.fixture
def raw_parcel_response():
    return {
        "displayFieldName": "PROP_ST_NAME",
        "fieldAliases": {
            "OBJECTID": "OBJECTID",
            "PID": "PID",
            "OWNER1": "OWNER1",
            "OWNER2": "OWNER2",
            "TAX_DISTRICT": "TAX DISTRICT",
            "CLASS_CODE": "CLASS CODE",
            "MAIL_ST_NO": "MAIL_ST_NO",
            "MAIL_ST_NAME": "MAIL_ST_NAME",
            "MAIL_ST_TYPE": "MAIL_ST_TYPE",
            "MAIL_2ND_ADDR": "MAIL_2ND_ADDR",
            "MAIL_2ND_ADDT": "MAIL_2ND_ADDT",
            "MAIL_CITY": "MAIL_CITY",
            "MAIL_STATE": "MAIL_STATE",
            "MAIL_ZIP": "MAIL_ZIP",
            "MAIL_COUNTRY": "MAIL_COUNTRY",
            "LEGAL_DESCR": "LEGAL DESCRIPTION",
            "SUBDIVISION": "SUBDIVISION",
            "ACREAGE": "DEEDED ACREAGE",
            "LEGAL_RESIDENCE": "LEGAL RESIDENCE",
            "OTHER": "OTHER",
            "AGR": "AGR",
            "DEED_BOOK_PAGE": "DEED BOOK PAGE",
            "PLAT_BOOK_PAGE": "PLAT BOOK PAGE",
            "SALE_PRICE": "SALE_PRICE",
            "RECORDED_DATE": "RECORDED_DATE",
            "DOC_DATE": "DOC_DATE",
        },
        "geometryType": "esriGeometryPolygon",
        "spatialReference": {"wkid": 2273, "latestWkid": 2273},
        "fields": [],
        "features": [
            {
                "attributes": {
                    "OBJECTID": 1,
                    "PID": "3970500692",
                    "OWNER1": "GLAVIS DANI LEIGH",
                    "OWNER2": "",
                    "TAX_DISTRICT": "4-3             ",
                    "CLASS_CODE": "101 - RESID-SFR                                                 ",
                    "MAIL_ST_NO": "7637",
                    "MAIL_ST_NAME": "HIGH MAPLE CIRCLE                                               ",
                    "MAIL_ST_TYPE": "        ",
                    "MAIL_2ND_ADDR": "        ",
                    "MAIL_2ND_ADDT": "        ",
                    "MAIL_CITY": "NORTH CHARLESTON                ",
                    "MAIL_STATE": "SC  ",
                    "MAIL_ZIP": "29418           ",
                    "MAIL_COUNTRY": "                                ",
                    "LEGAL_DESCR": "LOT 37",
                    "SUBDIVISION": " ",
                    "ACREAGE": 0.16,
                    "LEGAL_RESIDENCE": "Y",
                    "OTHER": "Y",
                    "AGR": "N",
                    "DEED_BOOK_PAGE": "1022-581",
                    "PLAT_BOOK_PAGE": " XXX-L110001 ",
                    "SALE_PRICE": 270000.0,
                    "RECORDED_DATE": 1628726400000,
                    "DOC_DATE": 1628640000000,
                },
                "geometry": {
                    "rings": [
                        [
                            [2282972.5878063738, 394271.15339459479],
                            [2282913.8214494437, 394291.16423550248],
                            [2282948.4476482868, 394398.45847891271],
                            [2283007.2628900707, 394378.59114645422],
                            [2282972.5878063738, 394271.15339459479],
                        ]
                    ]
                },
            }
        ],
        "exceededTransferLimit": True,
    }


def test_full_pipeline_deserialization(raw_parcel_response):
    response = ArcGISResponse.model_validate(raw_parcel_response)

    feature = response.features[0]
    attrs = feature.attributes

    assert response.exceededTransferLimit is True
    assert attrs.objectid == 1
    assert attrs.pid == "3970500692"
    assert attrs.owner1 == "GLAVIS DANI LEIGH"
    assert attrs.acreage == 0.16
    assert attrs.sale_price == 270000.0


def test_alias_mapping_and_primitive_types(raw_parcel_response):
    """Ensures raw dot-notation keys accurately map to snake_case attributes."""
    response = ArcGISResponse.model_validate(raw_parcel_response)
    attrs = response.features[0].attributes

    assert attrs.objectid == 1
    assert attrs.sale_price == 270000.0


def test_string_whitespace_and_empty_space_stripping(raw_parcel_response):
    """Ensures blank fields convert to None and text fields strip extra padding."""
    response = ArcGISResponse.model_validate(raw_parcel_response)
    attrs = response.features[0].attributes

    # Truncated or clean values
    assert attrs.owner1 == "GLAVIS DANI LEIGH"
    assert attrs.tax_district == "4-3"
    assert attrs.class_code == "101 - RESID-SFR"
    assert attrs.mail_st_name == "HIGH MAPLE CIRCLE"
    assert attrs.mail_city == "NORTH CHARLESTON"
    assert attrs.mail_state == "SC"
    assert attrs.mail_zip == "29418"
    assert (
        attrs.plat_book_page == "XXX-L110001"
    )  # Internal spaces kept, padding removed

    # Space strings or empty quotes converted completely to None
    assert attrs.mail_st_type is None
    assert attrs.owner2 is None
    assert attrs.mail_2nd_addr is None
    assert attrs.mail_2nd_addt is None
    assert attrs.mail_country is None
    assert attrs.subdivision is None


def test_epoch_milliseconds_transform_to_utc_datetime(raw_parcel_response):
    """Verifies huge bigint timestamps become valid timezone-aware datetimes."""
    response = ArcGISResponse.model_validate(raw_parcel_response)
    attrs = response.features[0].attributes

    raw_recorded = raw_parcel_response["features"][0]["attributes"]["RECORDED_DATE"]
    raw_doc = raw_parcel_response["features"][0]["attributes"]["DOC_DATE"]

    assert raw_recorded == 1628726400000
    assert raw_doc == 1628640000000

    expected_recorded = datetime.fromtimestamp(raw_recorded / 1000, tz=timezone.utc)
    expected_doc = datetime.fromtimestamp(raw_doc / 1000, tz=timezone.utc)

    assert attrs.recorded_date == expected_recorded
    assert attrs.doc_date == expected_doc


def test_missing_required_id_field_throws_validation_error(raw_parcel_response):
    """Ensures missing mandatory identifiers trigger immediate safe extraction failures."""
    # Delete the vital key from the nested dict structure
    del raw_parcel_response["features"][0]["attributes"]["OBJECTID"]

    with pytest.raises(ValidationError) as excinfo:
        ArcGISResponse.model_validate(raw_parcel_response)

    assert "OBJECTID" in str(excinfo.value)


def test_handles_multiple_features_in_payload():
    """Verify that multiple features in the 'features' array are processed correctly."""
    multi_record_json = {
        "features": [
            {
                "attributes": {
                    "OBJECTID": 1,
                    "PID": "001",
                }
            },
            {
                "attributes": {
                    "OBJECTID": 2,
                    "PID": "002",
                }
            },
        ]
    }

    # ACT
    response = ArcGISResponse.model_validate(multi_record_json)

    # ASSERT
    assert len(response.features) == 2
    assert response.features[0].attributes.objectid == 1
    assert response.features[1].attributes.objectid == 2

def test_out_of_range_epoch_milliseconds_become_none():
    raw_response = {
        "features": [
            {
                "attributes": {
                    "OBJECTID": 1,
                    "PID": "3970500692",
                    "RECORDED_DATE": -19879776000000,
                    "DOC_DATE": 19454496000000,
                }
            }
        ]
    }

    response = ArcGISResponse.model_validate(raw_response)
    attrs = response.features[0].attributes

    assert attrs.recorded_date is None
    assert attrs.doc_date is None

def test_valid_epoch_milliseconds_still_convert_to_datetime():
    raw_response = {
        "features": [
            {
                "attributes": {
                    "OBJECTID": 1,
                    "PID": "3970500692",
                    "RECORDED_DATE": 1628726400000,
                    "DOC_DATE": 1628640000000,
                }
            }
        ]
    }

    response = ArcGISResponse.model_validate(raw_response)
    attrs = response.features[0].attributes

    assert attrs.recorded_date == datetime.fromtimestamp(
        1628726400000 / 1000,
        tz=timezone.utc,
    )
    assert attrs.doc_date == datetime.fromtimestamp(
        1628640000000 / 1000,
        tz=timezone.utc,
    )