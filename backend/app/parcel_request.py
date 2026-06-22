import argparse
import time
from datetime import datetime, timezone

import requests
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from .config import settings
from .db import get_session
from .geometry import (
    AREA_COMPUTATION_METHOD,
    compute_acreage_from_esri_polygon,
    compute_area_sqft_from_esri_polygon,
)
from .models import (
    ArcGISErrorResponse,
    ArcGISResponse,
    Parcel,
    ParcelFetchParams,
    RecordsOnlyResponse,
)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
}


def fetch_page(
    params_model: ParcelFetchParams,
) -> ArcGISResponse | RecordsOnlyResponse | None:
    query_params = params_model.model_dump()

    try:
        response = requests.get(
            str(settings.URL), params=query_params, headers=headers, timeout=30
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
            error_data = ArcGISErrorResponse.model_validate(response_json)
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


def upsert_features(
    session: Session, validated_data: ArcGISResponse, snapshot_at: datetime
) -> tuple[int, int]:
    upserted_count = 0
    skipped_count = 0

    geometry_wkid = (
        validated_data.spatialReference.wkid
        if validated_data.spatialReference is not None
        else None
    )

    for feature in validated_data.features:
        incoming_record = feature.attributes

        validated_fields = incoming_record.model_dump(
            by_alias=False,
            mode="python",
        )

        if not validated_fields.get("pid"):
            skipped_count += 1
            continue

        validated_fields["snapshot_at"] = snapshot_at

        geometry_esri_json = (
            feature.geometry.model_dump() if feature.geometry is not None else None
        )

        validated_fields["geometry_esri_json"] = geometry_esri_json
        validated_fields["geometry_wkid"] = geometry_wkid

        if geometry_esri_json is not None:
            try:
                validated_fields["computed_area_sqft"] = (
                    compute_area_sqft_from_esri_polygon(geometry_esri_json)
                )
                validated_fields["computed_acreage"] = (
                    compute_acreage_from_esri_polygon(geometry_esri_json)
                )
                validated_fields["area_computation_method"] = AREA_COMPUTATION_METHOD
            except ValueError as e:
                print(
                    "⚠️ Geometry acreage skipped. "
                    f"OBJECTID={incoming_record.objectid}, "
                    f"PID={incoming_record.pid}, "
                    f"rings={len(geometry_esri_json.get('rings', []))}, "
                    f"error={e}"
                )

        stmt = insert(Parcel).values(**validated_fields)

        update_fields = {
            key: stmt.excluded[key] for key in validated_fields.keys() if key != "pid"
        }

        stmt = stmt.on_conflict_do_update(
            index_elements=[Parcel.pid],
            set_=update_fields,
        ).returning(Parcel.pid)

        upserted_pid = session.execute(stmt).scalar_one_or_none()

        if upserted_pid is None:
            skipped_count += 1
        else:
            upserted_count += 1

    session.commit()

    return upserted_count, skipped_count


def validate_parcel_service() -> bool:
    params_model = ParcelFetchParams(
        resultRecordCount=1,
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

    if first_feature.attributes.pid is None:
        print("❌ Parcel service response is missing PID.")
        return False

    print("✅ Parcel service validation passed.")
    return True


def crawl_all_parcels(page_size: int = 2000, delay_seconds: float = 0.5) -> None:
    if not validate_parcel_service():
        return

    snapshot_at = datetime.now(timezone.utc)

    offset = 0

    total_fetched = 0
    total_processed = 0
    total_skipped = 0

    session: Session = next(get_session())

    try:
        while True:
            params_model = ParcelFetchParams(
                resultOffset=offset, resultRecordCount=page_size
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
                processed_count, skipped_count = upsert_features(
                    session=session, validated_data=page_data, snapshot_at=snapshot_at
                )
            except Exception as e:
                session.rollback()
                print(f"❌ Processing/Database Error at offset {offset}: {e}")
                break

            total_fetched += fetched_count
            total_processed += processed_count
            total_skipped += skipped_count

            print(
                f"Done page offset={offset}. "
                f"Processed {processed_count} records. "
                f"Skipped {skipped_count} records."
            )

            print(
                f"Running totals: "
                f"fetched={total_fetched}, "
                f"processed={total_processed}, "
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--page-size", type=int, default=2000)
    parser.add_argument("--delay-seconds", type=float, default=0.5)

    args = parser.parse_args()

    crawl_all_parcels(page_size=args.page_size, delay_seconds=args.delay_seconds)
