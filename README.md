# Charleston County ArcGIS API Reference

This document explains how to use Charleston County’s ArcGIS REST endpoints programmatically, especially for pulling parcel data for property research.

Primary parcel service:

```text
https://gisccapps.charlestoncounty.org/arcgis/rest/services/GIS_VIEWER/Parcel_Search/MapServer
```

Parcel layer query endpoint:

```text
https://gisccapps.charlestoncounty.org/arcgis/rest/services/GIS_VIEWER/Parcel_Search/MapServer/4/query
```

---

# 1. ArcGIS REST Structure

ArcGIS Server is organized roughly like this:

```text
/arcgis/rest/services/
    ├── Folder
    │      ├── Service/MapServer
    │      │      ├── Layer 0
    │      │      ├── Layer 1
    │      │      └── Layer 4
```

## Folder

A folder is just an organizational container.

Example:

```text
GIS_VIEWER
```

Folders group related services together.

They are similar to directories or namespaces.

## Service

A service is the actual GIS endpoint.

Example:

```text
Parcel_Search/MapServer
```

A service can expose multiple layers.

## Layer

A layer is similar to a table or dataset inside the service.

For the parcel service:

```text
MapServer/4
```

Layer `4` is the parcel layer.

## Query Operation

To pull data from a layer, use:

```text
/query
```

Full endpoint:

```text
/MapServer/4/query
```

---

# 2. Useful Metadata URLs

## Service Metadata

```text
https://gisccapps.charlestoncounty.org/arcgis/rest/services/GIS_VIEWER/Parcel_Search/MapServer?f=pjson
```

Use this to inspect:

- available layers
- service capabilities
- max record count
- supported query formats

## Parcel Layer Metadata

```text
https://gisccapps.charlestoncounty.org/arcgis/rest/services/GIS_VIEWER/Parcel_Search/MapServer/4?f=pjson
```

Use this to inspect:

- field names
- field types
- geometry type
- object ID field
- supported query capabilities
- max record count

---

# 3. Important Parcel Fields

The field names are verbose because they come from joined county datasets.

## Technical ID

```text
FEATURES.SDE.P_POLY_PARCEL.OBJECTID
```

ArcGIS row ID.

Useful for:

- fetching by object ID
- pagination strategies
- deduping within one pull

Do not rely on this as the permanent real-world parcel ID.

## Parcel IDs

```text
FEATURES.SDE.P_POLY_PARCEL.PID
FEATURES.SDE.P_POLY_PARCEL.GPIN
```

Use these as long-term parcel identifiers.

## Acreage

```text
FEATURES.SDE.P_POLY_PARCEL.ACRES_CAL
FEATURES.SDE.CAMA.ACREAGE
```

`ACRES_CAL` is calculated from GIS geometry.

`ACREAGE` is the tax/CAMA recorded acreage.

For practical filtering, start with `ACRES_CAL`.

## Ownership

```text
FEATURES.SDE.CAMA.OWNER1
FEATURES.SDE.CAMA.OWNER2
```

Useful for identifying:

- individuals
- LLCs
- trusts
- estates
- family ownership

## Mailing Address

```text
FEATURES.SDE.CAMA.MAIL_ST_NO
FEATURES.SDE.CAMA.MAIL_ST_NAME
FEATURES.SDE.CAMA.MAIL_ST_TYPE
FEATURES.SDE.CAMA.MAIL_CITY
FEATURES.SDE.CAMA.MAIL_STATE
FEATURES.SDE.CAMA.MAIL_ZIP
FEATURES.SDE.CAMA.MAIL_COUNTRY
```

These are extremely useful for detecting absentee ownership.

A mailing address different from the property address can indicate:

- absentee owner
- rental/investment property
- inherited property
- owner moved away
- business-owned parcel

## Sale / Ownership Date

```text
FEATURES.SDE.CAMA.RECORDED_DATE
FEATURES.SDE.CAMA.DOC_DATE
```

`RECORDED_DATE` is usually the best proxy for ownership start date.

Use it to calculate years owned.

## Sale Price

```text
FEATURES.SDE.CAMA.SALE_PRICE
```

Useful but not always reliable.

Some transfers may be family transfers, deed corrections, estate transfers, or non-market transactions.

## Deed Reference

```text
FEATURES.SDE.CAMA.DEED_BOOK_PAGE
FEATURES.SDE.CAMA.PLAT_BOOK_PAGE
```

Useful for deeper research in register-of-deeds systems.

---

# 4. Core Query Parameters

The `/query` endpoint accepts HTTP GET or POST parameters.

## `f`

Output format.

Common values:

```text
json
pjson
geojson
```

Recommended default:

```text
f=json
```

Use `geojson` when pulling geometry for GIS tools.

---

## `where`

SQL-like filter.

All records:

```text
where=1=1
```

Acreage filter:

```text
where=FEATURES.SDE.P_POLY_PARCEL.ACRES_CAL >= 0.75
```

Older ownership date example:

```text
where=FEATURES.SDE.CAMA.RECORDED_DATE < DATE '2005-01-01'
```

Date syntax can vary by ArcGIS backend. If date filters are unreliable, pull the data and filter locally in Python.

---

## `outFields`

Fields to return.

All fields:

```text
outFields=*
```

Specific fields:

```text
outFields=FEATURES.SDE.CAMA.OWNER1,FEATURES.SDE.CAMA.RECORDED_DATE
```

For bulk pulls, avoid `*` once you know the fields you need.

---

## `returnGeometry`

Whether to include parcel shapes.

```text
returnGeometry=false
```

Recommended for first-pass data pulls.

Parcel polygons are heavy.

Use:

```text
returnGeometry=true
```

only when you need shapes for mapping or spatial filtering.

---

## `outSR`

Output spatial reference.

For normal latitude/longitude:

```text
outSR=4326
```

Use this when returning geometry or GeoJSON.

---

## `resultOffset`

Starting row for pagination.

Examples:

```text
resultOffset=0
resultOffset=1000
resultOffset=2000
```

---

## `resultRecordCount`

Number of records to return in one page.

Typical max:

```text
resultRecordCount=1000
```

Check layer metadata for the actual max record count.

---

## `returnCountOnly`

Returns only the count of matching records.

Example:

```text
returnCountOnly=true
```

Useful for testing filters.

---

## `returnIdsOnly`

Returns only object IDs for matching records.

Example:

```text
returnIdsOnly=true
```

Very useful for reliable bulk pulling.

Object ID queries are often not limited the same way full feature responses are.

---

## `objectIds`

Fetch specific records by object ID.

Example:

```text
objectIds=123,456,789
```

Useful after calling `returnIdsOnly=true`.

---

## `orderByFields`

Sort results.

Example:

```text
orderByFields=FEATURES.SDE.CAMA.RECORDED_DATE ASC
```

or:

```text
orderByFields=FEATURES.SDE.P_POLY_PARCEL.ACRES_CAL DESC
```

---

# 5. Basic Query Example

Pull five parcel records without geometry:

```text
https://gisccapps.charlestoncounty.org/arcgis/rest/services/GIS_VIEWER/Parcel_Search/MapServer/4/query?where=1%3D1&outFields=*&returnGeometry=false&f=json&resultRecordCount=5
```

Python:

```python
import requests

url = "https://gisccapps.charlestoncounty.org/arcgis/rest/services/GIS_VIEWER/Parcel_Search/MapServer/4/query"

params = {
    "f": "json",
    "where": "1=1",
    "outFields": "*",
    "returnGeometry": "false",
    "resultRecordCount": 5,
}

r = requests.get(url, params=params, timeout=30)
r.raise_for_status()
data = r.json()

for feature in data["features"]:
    print(feature["attributes"])
```

---

# 6. Pagination With `resultOffset`

Use this for a simple first ingestion pipeline.

```python
import requests
import pandas as pd

url = "https://gisccapps.charlestoncounty.org/arcgis/rest/services/GIS_VIEWER/Parcel_Search/MapServer/4/query"

page_size = 1000
offset = 0
rows = []

while True:
    params = {
        "f": "json",
        "where": "1=1",
        "outFields": "*",
        "returnGeometry": "false",
        "resultOffset": offset,
        "resultRecordCount": page_size,
    }

    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()

    features = data.get("features", [])
    if not features:
        break

    rows.extend(feature["attributes"] for feature in features)

    if len(features) < page_size:
        break

    offset += page_size

    print(f"Pulled {len(rows)} records")

df = pd.DataFrame(rows)
df.to_csv("charleston_parcels.csv", index=False)
```

---

# 7. More Reliable Bulk Pull: Object IDs First

This is better for larger production-style pulls.

Step 1: get all matching object IDs.

Step 2: fetch chunks by `objectIds`.

```python
import requests
import pandas as pd

url = "https://gisccapps.charlestoncounty.org/arcgis/rest/services/GIS_VIEWER/Parcel_Search/MapServer/4/query"

session = requests.Session()

id_params = {
    "f": "json",
    "where": "1=1",
    "returnIdsOnly": "true",
}

r = session.get(url, params=id_params, timeout=30)
r.raise_for_status()
object_ids = r.json()["objectIds"]

print(f"Found {len(object_ids)} object IDs")


def chunks(items, size):
    for i in range(0, len(items), size):
        yield items[i:i + size]

rows = []

for chunk in chunks(object_ids, 1000):
    params = {
        "f": "json",
        "objectIds": ",".join(map(str, chunk)),
        "outFields": "*",
        "returnGeometry": "false",
    }

    r = session.get(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()

    rows.extend(feature["attributes"] for feature in data.get("features", []))
    print(f"Pulled {len(rows)} records")

df = pd.DataFrame(rows)
df.to_csv("charleston_parcels.csv", index=False)
```

---

# 8. Spatial Query By Bounding Box

Use this to pull parcels within a defined area.

Bounding box format:

```text
xmin,ymin,xmax,ymax
```

For longitude/latitude, that means:

```text
west,south,east,north
```

Example:

```python
import requests
import pandas as pd

url = "https://gisccapps.charlestoncounty.org/arcgis/rest/services/GIS_VIEWER/Parcel_Search/MapServer/4/query"

bbox = "-79.99,32.70,-79.92,32.78"

params = {
    "f": "json",
    "where": "FEATURES.SDE.P_POLY_PARCEL.ACRES_CAL >= 0.75",
    "outFields": "*",
    "returnGeometry": "false",
    "geometry": bbox,
    "geometryType": "esriGeometryEnvelope",
    "inSR": "4326",
    "spatialRel": "esriSpatialRelIntersects",
    "resultRecordCount": 1000,
}

r = requests.get(url, params=params, timeout=30)
r.raise_for_status()
data = r.json()

rows = [feature["attributes"] for feature in data.get("features", [])]
df = pd.DataFrame(rows)
```

This pulls parcels that intersect the bounding box.

It may include parcels partially outside your exact target area.

---

# 9. Spatial Query With Geometry Returned

Use this when you want to map parcels or filter more precisely in GeoPandas.

```python
params = {
    "f": "geojson",
    "where": "FEATURES.SDE.P_POLY_PARCEL.ACRES_CAL >= 0.75",
    "outFields": "*",
    "returnGeometry": "true",
    "outSR": "4326",
    "geometry": "-79.99,32.70,-79.92,32.78",
    "geometryType": "esriGeometryEnvelope",
    "inSR": "4326",
    "spatialRel": "esriSpatialRelIntersects",
    "resultRecordCount": 1000,
}
```

For GIS analysis, save as GeoJSON:

```python
import json

with open("parcels.geojson", "w") as f:
    json.dump(data, f)
```

---

# 10. Filtering By Acreage

Use the GIS-calculated acreage field first:

```text
FEATURES.SDE.P_POLY_PARCEL.ACRES_CAL
```

Examples:

```text
FEATURES.SDE.P_POLY_PARCEL.ACRES_CAL >= 0.5
```

```text
FEATURES.SDE.P_POLY_PARCEL.ACRES_CAL >= 1.0
```

```text
FEATURES.SDE.P_POLY_PARCEL.ACRES_CAL BETWEEN 0.5 AND 5
```

If `BETWEEN` is unsupported, use:

```text
FEATURES.SDE.P_POLY_PARCEL.ACRES_CAL >= 0.5 AND FEATURES.SDE.P_POLY_PARCEL.ACRES_CAL <= 5
```

---

# 11. Ownership Date / Years Owned

Use:

```text
FEATURES.SDE.CAMA.RECORDED_DATE
```

Convert in Python.

ArcGIS date fields may come back as epoch milliseconds.

```python
import pandas as pd

col = "FEATURES.SDE.CAMA.RECORDED_DATE"

df["recorded_date"] = pd.to_datetime(df[col], unit="ms", errors="coerce")

df["years_owned"] = (
    (pd.Timestamp.today() - df["recorded_date"]).dt.days / 365.25
).round(1)
```

If the date already comes back as a string, use:

```python
df["recorded_date"] = pd.to_datetime(df[col], errors="coerce")
```

Then filter:

```python
long_owned = df[df["years_owned"] >= 20]
```

---

# 12. Candidate Scoring Ideas

For your utility property search, useful signals include:

| Signal | Why it matters |
|---|---|
| Owned 20+ years | High equity, possible aging owner |
| Mailing address differs | Absentee ownership |
| Out-of-state mailing address | Possible low local involvement |
| Low improvement value | Underutilized site |
| Large parcel | More utility |
| Existing structure | Useful workshop/storage potential |
| Commercial/industrial use | Better fit for storage/workshop |
| No recent investment | Possible operational fatigue |

Simple scoring example:

```python
df["score"] = 0

df.loc[df["years_owned"] >= 20, "score"] += 30
df.loc[df["FEATURES.SDE.P_POLY_PARCEL.ACRES_CAL"] >= 0.75, "score"] += 10
df.loc[df["FEATURES.SDE.CAMA.MAIL_STATE"].ne("SC"), "score"] += 10
```

You will need parcel situs/property address fields from another layer or enrichment source to compare mailing address vs property address.

---

# 13. Recommended Development Workflow

## Step 1
Inspect layer metadata:

```text
/MapServer/4?f=pjson
```

## Step 2
Pull a small sample:

```text
where=1=1
resultRecordCount=5
returnGeometry=false
```

## Step 3
Build a local schema mapping.

Example:

```python
FIELD_MAP = {
    "FEATURES.SDE.P_POLY_PARCEL.PID": "pid",
    "FEATURES.SDE.P_POLY_PARCEL.GPIN": "gpin",
    "FEATURES.SDE.P_POLY_PARCEL.ACRES_CAL": "acres_cal",
    "FEATURES.SDE.CAMA.OWNER1": "owner1",
    "FEATURES.SDE.CAMA.OWNER2": "owner2",
    "FEATURES.SDE.CAMA.MAIL_CITY": "mail_city",
    "FEATURES.SDE.CAMA.MAIL_STATE": "mail_state",
    "FEATURES.SDE.CAMA.RECORDED_DATE": "recorded_date_raw",
    "FEATURES.SDE.CAMA.SALE_PRICE": "sale_price",
}

df = df.rename(columns=FIELD_MAP)
```

## Step 4
Pull your target area only.

Start with bounding boxes.

## Step 5
Store results locally.

Good options:

- CSV for quick experiments
- SQLite for simple local database
- DuckDB for analytics
- PostgreSQL/PostGIS for serious spatial work
- Parquet for efficient file storage

## Step 6
Add scoring and manual review.

Do not trust the score blindly.

Use it to prioritize field inspection.

---

# 14. Practical Warnings

## Do not bulk pull geometry unless needed

This is slow and heavy:

```text
outFields=*
returnGeometry=true
```

Start with attributes only.

## Do not treat OBJECTID as permanent

Use OBJECTID for fetching.

Use PID/GPIN for long-term parcel tracking.

## County schemas may change

Keep field mapping isolated in one place.

## Recorded date is not perfect

A recent recorded date can reflect:

- trust transfer
- family transfer
- estate update
- LLC restructuring
- deed correction

Manual review still matters.

## Public data does not equal seller motivation

Use the data to rank probabilities, not to assume distress.

---

# 15. Useful Official Documentation

Esri ArcGIS REST API documentation:

```text
https://developers.arcgis.com/rest/
```

Query Feature Service Layer reference:

```text
https://developers.arcgis.com/rest/services-reference/enterprise/query-feature-service-layer/
```

Query features guide:

```text
https://developers.arcgis.com/documentation/portal-and-data-services/data-services/feature-services/query-features/
```

Even though Charleston uses `MapServer`, the query parameters are very similar across ArcGIS REST query endpoints.

---

# 16. Best Starting Point For Your Project

Start with this pipeline:

1. Define a bounding box around the nearby areas that are actually useful to you.
2. Query parcels with `ACRES_CAL >= 0.5` or `>= 0.75`.
3. Pull attributes only.
4. Calculate years owned from `RECORDED_DATE`.
5. Rank by ownership duration, acreage, owner type, and mailing address.
6. Manually inspect the top 25–50 properties.
7. Only then add geometry, flood, zoning, permit, and tax enrichment.

The goal is not to scrape everything.

The goal is to build a focused local intelligence system for properties that could realistically become your nearby workshop/storage site.

