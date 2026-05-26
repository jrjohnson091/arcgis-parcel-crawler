import requests
import pandas as pd

URL = "https://gisccapps.charlestoncounty.org/arcgis/rest/services/GIS_VIEWER/Parcel_Search/MapServer/4/query"

params = {
    # "where": "1=1",
    # "where": "FEATURES.SDE.CAMA.OWNER1 LIKE 'JOHNSON%JOSHUA%'",
    "where": "FEATURES.SDE.CAMA.OWNER1 LIKE 'MURRAY%MATT%'",
    "outFields": "*",
    "returnGeometry": "false",
    "f": "json",
    # "returnCountOnly": "true"
    # "resultOffset": 0,
    # "resultRecordCount": 1, # 1000,
}

rows = []

# while True:
r = requests.get(URL, params=params, timeout=30)
r.raise_for_status()
data = r.json()
# print(data)

features = data.get("features", [])
# # if not features:
# #     break

# rows.extend([f["attributes"] for f in features])
# print([f["attributes"]["FEATURES.SDE.P_POLY_PARCEL.PID"] for f in features])
print([f["attributes"]["FEATURES.SDE.CAMA.MAIL_ZIP"] for f in features])
# print([[f["attributes"]["FEATURES.SDE.CAMA.OWNER1"],f["attributes"]["FEATURES.SDE.CAMA.OWNER2"]]  for f in features])



# # if not data.get("exceededTransferLimit"):
# #     break

# params["resultOffset"] += 1000
# print("pulled", len(rows))

# df = pd.DataFrame(rows)
# df.to_csv("charleston_parcels.csv", index=False)

# print(df.shape)
# print(df.columns.tolist())