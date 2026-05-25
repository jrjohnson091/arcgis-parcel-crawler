import requests

from .config import settings
from .models import ArcGIS_Error_Response, ArcGISResponse, Params, RecordsOnlyResponse

params_model = Params(
    # where="FEATURES.SDE_CAMA.OWNER1 LIKE 'JOHNSON%JOSHUA%'",
    resultRecordCount=1,
    returnCountOnly=False,
)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
}

params_model = Params(
    # where="FEATURES.SDE_CAMA.OWNER1 LIKE 'JOHNSON%JOSHUA%'",
    resultRecordCount=1,
    returnCountOnly=False,  # This can safely be toggled to True now!
)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
}

def main():
    query_params = params_model.model_dump()
    response = requests.get(settings.url, params=query_params, headers=headers, timeout=30)

    response_json = response.json()
    print(response_json)

    # 1. CHECK FIRST: Did the server return an embedded database error?
    if "error" in response_json:
        try:
            error_data = ArcGIS_Error_Response.model_validate(response_json)
            print(f"❌ ArcGIS Server Error (Code {error_data.error.code}):")
            print(f"   Message: {error_data.error.message}")
        except Exception:
            print(f"Raw Error Payload: {response_json}")
        return  # Exit safely without crashing the script

    # 2. CHECK SECOND: Did we request a count only?
    if "count" in response_json:
        try:
            count_data = RecordsOnlyResponse.model_validate(response_json)
            print(f"📊 Query Match Count: {count_data.count}")
            print(count_data.model_dump_json(indent=4))
        except Exception as e:
            print(f"Pydantic Count Validation Error: {e}")
        return  # Exit safely since there are no features to parse

    # 3. PROCEED TO FEATURES: If no error or count keys exist, validate features dataset
    try:
        validated_data = ArcGISResponse.model_validate(response_json)
        print(f" Success! Processed {len(validated_data.features)} parcels.")
        print(validated_data.model_dump_json(indent=4))
    except Exception as e:
        print(f"Pydantic Validation Error: {e}")