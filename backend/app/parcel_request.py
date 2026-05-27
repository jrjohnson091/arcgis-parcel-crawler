import requests
# 1. Added the missing 'select' import from sqlmodel
from sqlmodel import Session
from sqlalchemy.dialects.postgresql import insert

from .config import settings
from .db import get_session
from .models import (
    ArcGIS_Error_Response,
    ArcGISResponse,
    Attributes,
    Params,
    RecordsOnlyResponse,
)

params_model = Params(
    resultRecordCount=500,
    returnCountOnly=False,
)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
}

def main():
    query_params = params_model.model_dump()
    response = requests.get(settings.URL, params=query_params, headers=headers, timeout=30)

    response_json = response.json()

    # 1. CHECK FIRST: Did the server return an embedded database error?
    if "error" in response_json:
        try:
            error_data = ArcGIS_Error_Response.model_validate(response_json)
            print(f"❌ ArcGIS Server Error (Code {error_data.error.code}):")
            print(f"   Message: {error_data.error.message}")
        except Exception:
            print(f"Raw Error Payload: {response_json}")
        return

    # 2. CHECK SECOND: Did we request a count only?
    if "count" in response_json:
        try:
            count_data = RecordsOnlyResponse.model_validate(response_json)
            print(f"📊 Query Match Count: {count_data.count}")
            print(count_data.model_dump_json(indent=4))
        except Exception as e:
            print(f"Pydantic Count Validation Error: {e}")
        return

    # 3. PROCEED TO FEATURES
    try:
        validated_data = ArcGISResponse.model_validate(response_json)
        print(f"✅ Success! Parsed {len(validated_data.features)} parcels from API.")

        session: Session = next(get_session())
        
        try:
            inserted_count = 0
            skipped_count = 0
            
            for feature in validated_data.features:
                incoming_record = feature.attributes
                
                # Extract the clean dictionary directly using mode="json" 
                # This ensures your dates are passed as clean ISO-strings rather than raw bigints
                validated_fields = incoming_record.model_dump(by_alias=False, mode="json")
                if "id" in validated_fields:
                    del validated_fields["id"]

                # Build the PostgreSQL raw insert statement
                stmt = insert(Attributes).values(**validated_fields)
                
                # Tell PostgreSQL to ignore the record if the unique OBJECTID already exists
                skip_stmt = stmt.on_conflict_do_nothing(
                    index_elements=[Attributes.features_sde_p_poly_parcel_objectid]
                )
                
                # Execute transaction directly
                result = session.exec(skip_stmt)
                
                if result.rowcount > 0:
                    inserted_count += 1
                else:
                    skipped_count += 1
            
            # Safely batch commit the new items
            session.commit()
            print(f"💾 Done! Inserted {inserted_count} new records. Skipped {skipped_count} existing records.")
            
        finally:
            session.close()

    except Exception as e:
        print(f"❌ Processing/Database Error: {e}")