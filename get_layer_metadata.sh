for id in 61 21 27 60 57; do
  echo "===== QUERY TEST $id ====="
  curl -s -G "$BASE/$id/query" \
    --data-urlencode "where=1=1" \
    --data-urlencode "outFields=*" \
    --data-urlencode "returnGeometry=false" \
    --data-urlencode "resultRecordCount=1" \
    --data-urlencode "f=json" \
    | jq '{fields:[.fields[]?.name], sample:.features[0].attributes, error:.error}'
done