# Charleston County ArcGIS API Reference

This document explains how to use Charleston County's ArcGIS REST endpoints programmatically, especially for pulling parcel data for property research.

---

# Service Change Notice

Charleston County migrated from the legacy parcel service to a newer service during development of this project.

Legacy parcel service:

```text
https://gisccapps.charlestoncounty.org/arcgis/rest/services/GIS_VIEWER/Parcel_Search/MapServer
```

Current parcel service:

```text
https://gisccapps.charlestoncounty.org/arcgis/rest/services/GIS_VIEWER/New_Parcel_Search/MapServer
```

Legacy parcel layer:

```text
MapServer/4
```

Current parcel layer:

```text
MapServer/61
```

Applications should not hardcode assumptions about layer IDs or field names. Charleston County has already changed both once.

---

# Current Production Endpoints

## Service Metadata

```text
https://gisccapps.charlestoncounty.org/arcgis/rest/services/GIS_VIEWER/New_Parcel_Search/MapServer?f=pjson
```

## Parcel Layer Metadata

```text
https://gisccapps.charlestoncounty.org/arcgis/rest/services/GIS_VIEWER/New_Parcel_Search/MapServer/61?f=pjson
```

## Parcel Query Endpoint

```text
https://gisccapps.charlestoncounty.org/arcgis/rest/services/GIS_VIEWER/New_Parcel_Search/MapServer/61/query
```

---

# ArcGIS REST Structure

ArcGIS Server is organized roughly like this:

```text
/arcgis/rest/services/
    ├── Folder
    │      ├── Service/MapServer
    │      │      ├── Layer 0
    │      │      ├── Layer 1
    │      │      └── Layer 61
```

## Folder

Example:

```text
GIS_VIEWER
```

Folders are organizational containers used to group services.

## Service

Example:

```text
New_Parcel_Search/MapServer
```

A service can expose multiple layers.

## Layer

Example:

```text
MapServer/61
```

Layer 61 currently contains Charleston County parcel data.

## Query Operation

To retrieve data:

```text
/query
```

Full endpoint:

```text
/MapServer/61/query
```

---

# Field Naming Differences

The legacy parcel service returned fully-qualified joined field names:

```text
FEATURES.SDE.P_POLY_PARCEL.PID
FEATURES.SDE.CAMA.OWNER1
FEATURES.SDE.CAMA.RECORDED_DATE
```

The current service returns simplified field names:

```text
PID
OWNER1
RECORDED_DATE
```

Example current response:

```json
{
  "OBJECTID": 1,
  "PID": "3970500692",
  "OWNER1": "GLAVIS DANI LEIGH",
  "SALE_PRICE": 270000.0,
  "RECORDED_DATE": 1628726400000
}
```

This significantly simplifies schema design.

---

# Important Current Fields

## Technical Identifier

```text
OBJECTID
```

ArcGIS row identifier.

Useful for:

- pagination
- deduplication
- incremental crawling

Do not treat as a permanent parcel identifier.

## Parcel Identifier

```text
PID
```

Primary parcel identifier returned by the current service.

## Ownership

```text
OWNER1
OWNER2
```

Useful for identifying:

- individuals
- LLCs
- trusts
- estates
- corporate ownership

## Mailing Address

```text
MAIL_ST_NO
MAIL_ST_NAME
MAIL_ST_TYPE
MAIL_CITY
MAIL_STATE
MAIL_ZIP
MAIL_COUNTRY
```

Useful for absentee-owner analysis.

## Acreage

```text
ACREAGE
```

Current acreage value returned by the service.

## Sale Price

```text
SALE_PRICE
```

Useful but should not be assumed to represent an arms-length transaction.

## Ownership Dates

```text
RECORDED_DATE
DOC_DATE
```

Important for ownership-duration calculations.

---

# ArcGIS Date Handling

Charleston County currently returns ArcGIS dates as Unix epoch milliseconds.

Example:

```text
1628726400000
```

Convert using:

```python
from datetime import datetime, timezone

datetime.fromtimestamp(
    1628726400000 / 1000,
    tz=timezone.utc,
)
```

Result:

```text
2021-08-12 00:00:00+00:00
```

Never assume ArcGIS date fields are ISO-8601 strings.

---

# Current Service Limits

Current metadata reports:

```text
maxRecordCount = 2000
```

Recommended page size:

```text
resultRecordCount=2000
```

Always verify against service metadata because administrators can change this value.

---

# Recommended Startup Validation

Before beginning a full crawl:

1. Query a single parcel.
2. Verify at least one feature is returned.
3. Verify OBJECTID exists.
4. Validate against local Pydantic schemas.
5. Fail fast if validation fails.

Example:

```python
params = {
    "where": "1=1",
    "outFields": "*",
    "returnGeometry": False,
    "resultRecordCount": 1,
    "f": "json",
}
```

This protects the crawler from silent county schema changes.

---

# Basic Query Example

```python
import requests

url = (
    "https://gisccapps.charlestoncounty.org/"
    "arcgis/rest/services/"
    "GIS_VIEWER/New_Parcel_Search/"
    "MapServer/61/query"
)

params = {
    "where": "1=1",
    "outFields": "*",
    "returnGeometry": False,
    "resultRecordCount": 1,
    "f": "json",
}

response = requests.get(url, params=params, timeout=30)
response.raise_for_status()

data = response.json()

print(data["features"][0]["attributes"])
```

---

# Lessons Learned During Development

1. Charleston County changed parcel services from `Parcel_Search` to `New_Parcel_Search`.
2. The parcel layer moved from Layer 4 to Layer 61.
3. Field names were simplified dramatically.
4. ArcGIS date fields are returned as epoch milliseconds.
5. The ArcGIS Web Adaptor can occasionally return HTML error pages when backend GIS servers are unavailable.
6. Production crawlers should validate the service before beginning large data pulls.
7. Schema validation tests using real API responses are invaluable for detecting county-side changes.

---

# Recommended Development Workflow

## Step 1

Inspect service metadata:

```text
/MapServer?f=pjson
```

## Step 2

Inspect layer metadata:

```text
/MapServer/61?f=pjson
```

## Step 3

Pull a single record:

```text
where=1=1
resultRecordCount=1
returnGeometry=false
```

## Step 4

Update schema mappings and validation tests.

## Step 5

Validate the service before crawling.

## Step 6

Run paginated crawls.

## Step 7

Store results in PostgreSQL for analysis.

---

# Useful Official Documentation

ArcGIS REST API:

https://developers.arcgis.com/rest/

Query Feature Layer:

https://developers.arcgis.com/rest/services-reference/enterprise/query-feature-service-layer/

Query Features Guide:

https://developers.arcgis.com/documentation/portal-and-data-services/data-services/feature-services/query-features/

Even though Charleston County exposes a MapServer endpoint, the query parameters are nearly identical to FeatureServer query operations.