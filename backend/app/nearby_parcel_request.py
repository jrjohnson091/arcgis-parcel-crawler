import requests

from .config import settings
from .models import (
    NearbyParcelCountParams,
    NearbyParcelIdsParams,
    ObjectIdsOnlyResponse,
    RecordsOnlyResponse,
)

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
}


def fetch_nearby_count(
    params_model: NearbyParcelCountParams,
) -> RecordsOnlyResponse | None:

    try:
        response = requests.get(
            settings.URL,
            params=params_model.to_query_params(),
            headers=headers,
            timeout=30,
        )

        response.raise_for_status()
        response_json = response.json()

    except Exception as e:
        print(f"❌ Request Error: {e}")
        return None

    try:
        return RecordsOnlyResponse.model_validate(response_json)
    except Exception as e:
        print(f"❌ Validation Error: {e}")
        return None


def fetch_nearby_ids(
    params_model: NearbyParcelIdsParams,
) -> ObjectIdsOnlyResponse | None:

    try:
        response = requests.get(
            settings.URL,
            params=params_model.to_query_params(),
            headers=headers,
            timeout=30,
        )

        response.raise_for_status()
        response_json = response.json()

    except Exception as e:
        print(f"❌ Request Error: {e}")
        return None

    try:
        return ObjectIdsOnlyResponse.model_validate(response_json)
    except Exception as e:
        print(f"❌ Validation Error: {e}")
        return None
