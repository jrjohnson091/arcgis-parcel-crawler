import time

import requests
from sqlalchemy.dialects.postgresql import insert
from sqlmodel import Session

from .config import settings
from .db import get_session
from .models import (
    ArcGIS_Error_Response,
    ArcGISResponse,
    Attributes,
    Params,
    RecordsOnlyResponse,
)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
}


def fetch_page(params_model: Params) -> ArcGISResponse | RecordsOnlyResponse | None:
    query_params = params_model.model_dump()

    try:
        response = requests.get(
            settings.URL, params=query_params, headers=headers, timeout=30
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ Request Error: {e}")
        return None

    content_type = response.headers.get("Content-Type", "")

    if "application/json" not in content_type.lower():
        print("❌ Non-JSON response from ArcGIS server.")
        print(f"   Status Code: {response.status_code}")
        print(f"   Content-Type: {content_type}")
        print(f"   First 300 chars: {response.text[:300]}")
        return None

    try:
        response_json = response.json()

    except ValueError as e:
        print(f"❌ JSON Decode Error: {e}")
        print(f"   First 300 chars: {response.text[:300]}")
        return None

    if "error" in response_json:
        try:
            error_data = ArcGIS_Error_Response.model_validate(response_json)
            print(f"❌ ArcGIS Server Error (Code {error_data.error.code}):")
            print(f"   Message: {error_data.error.message}")
        except Exception:
            print(f"Raw Error Payload: {response_json}")
        return None

    if "count" in response_json:
        try:
            count_data = RecordsOnlyResponse.model_validate(response_json)
            print(f"📊 Query Match Count: {count_data.count}")
            return count_data
        except Exception as e:
            print(f"Pydantic Count Validation Error: {e}")
            return None

    try:
        return ArcGISResponse.model_validate(response_json)
    except Exception as e:
        print(f"❌ Pydantic Feature Validation Error: {e}")
        return None


def insert_features(
    session: Session, validated_data: ArcGISResponse
) -> tuple[int, int]:
    inserted_count = 0
    skipped_count = 0

    for feature in validated_data.features:
        incoming_record = feature.attributes

        validated_fields = incoming_record.model_dump(
            by_alias=False,
            mode="json",
        )

        if "id" in validated_fields:
            del validated_fields["id"]

        stmt = insert(Attributes).values(**validated_fields)

        skip_stmt = stmt.on_conflict_do_nothing(
            index_elements=[
                Attributes.objectid,
            ]
        )

        result = session.exec(skip_stmt)

        if result.rowcount and result.rowcount > 0:
            inserted_count += 1
        else:
            skipped_count += 1

    session.commit()

    return inserted_count, skipped_count


def validate_parcel_service() -> bool:
    params_model = Params(
        resultRecordCount=1,
        returnCountOnly=False,
    )

    page_data = fetch_page(params_model)

    if page_data is None:
        print("❌ Parcel service validation failed.")
        return False

    if isinstance(page_data, RecordsOnlyResponse):
        print("❌ Parcel service returned count-only data during validation.")
        return False

    if not page_data.features:
        print("❌ Parcel service validation returned no features.")
        return False

    first_feature = page_data.features[0]

    if first_feature.attributes.objectid is None:
        print("❌ Parcel service response is missing OBJECTID.")
        return False

    print("✅ Parcel service validation passed.")
    return True


def crawl_all_parcels(page_size: int = 2000, delay_seconds: float = 0.5) -> None:
    if not validate_parcel_service():
        return

    offset = 0

    total_fetched = 0
    total_inserted = 0
    total_skipped = 0

    session: Session = next(get_session())

    try:
        while True:
            params_model = Params(
                resultOffset=offset, resultRecordCount=page_size, returnCountOnly=False
            )

            page_data = fetch_page(params_model)

            if page_data is None:
                print("Stopping crawl because page fetch failed.")
                break

            if isinstance(page_data, RecordsOnlyResponse):
                print("Stopping crawl because API returned count-only response.")
                break

            fetched_count = len(page_data.features)

            print(f"✅ Parsed {fetched_count} parcels from API at offset {offset}.")

            if fetched_count == 0:
                print("No more records returned.")
                break

            try:
                inserted_count, skipped_count = insert_features(
                    session=session,
                    validated_data=page_data,
                )
            except Exception as e:
                session.rollback()
                print(f"❌ Processing/Database Error at offset {offset}: {e}")
                break

            total_fetched += fetched_count
            total_inserted += inserted_count
            total_skipped += skipped_count

            print(
                f"Done page offset={offset}. "
                f"Inserted {inserted_count} new records. "
                f"Skipped {skipped_count} existing records."
            )

            print(
                f"Running totals: "
                f"fetched={total_fetched}, "
                f"inserted={total_inserted}, "
                f"skipped={total_skipped}"
            )

            if not page_data.exceededTransferLimit:
                print("Final page reached.")
                break

            offset += page_size
            time.sleep(delay_seconds)

    finally:
        session.close()


def main() -> None:
    crawl_all_parcels()
