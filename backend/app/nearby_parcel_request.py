from itertools import batched

import requests

from .config import settings
from .models import (
    NearbyParcelCountParams,
    NearbyParcelIdsParams,
    ObjectIdsOnlyResponse,
    PidLookupParams,
    PidOnlyResponse,
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
            str(settings.URL),
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
            str(settings.URL),
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


def fetch_pids(object_ids: list[int], batch_size: int = 500) -> list[str]:
    all_pids: list[str] = []
    
    for object_id_batch in batched(object_ids, batch_size):
        params_model = PidLookupParams(
            object_ids=object_id_batch,
        )
        try:
            response = requests.get(
                str(settings.URL),
                params=params_model.to_query_params(),
                headers=headers,
                timeout=30,
            )
            response.raise_for_status()
            response_json = response.json()
        except Exception as e:
            print(f"❌ Request Error: {e}")
            continue

        try:
            parsed = PidOnlyResponse.model_validate(response_json)
        except Exception as e:
            print(f"❌ Validation Error: {e}")
            continue

        all_pids.extend(
            feature.attributes.pid
            for feature in parsed.features
            if feature.attributes.pid
        )

    return all_pids
