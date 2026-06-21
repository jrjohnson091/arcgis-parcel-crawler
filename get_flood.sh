BASE="https://gisccapps.charlestoncounty.org/arcgis/rest/services/GIS_VIEWER/New_Parcel_Search/MapServer"
PID="4310700012"

GEOM=$(curl -s -G "$BASE/61/query" \
  --data-urlencode "where=PID='$PID'" \
  --data-urlencode "returnGeometry=true" \
  --data-urlencode "outFields=PID" \
  --data-urlencode "f=json" \
| jq -c '.features[0].geometry')

curl -G "$BASE/57/query" \
  --data-urlencode "geometry=$GEOM" \
  --data-urlencode "geometryType=esriGeometryPolygon" \
  --data-urlencode "spatialRel=esriSpatialRelIntersects" \
  --data-urlencode "outFields=FLD_ZONE,FLOODWAY,SFHA_TF,ZONE" \
  --data-urlencode "returnGeometry=false" \
  --data-urlencode "f=json" \
| jq .