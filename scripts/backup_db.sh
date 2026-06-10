#!/usr/bin/env bash
set -euo pipefail

mkdir -p backups

docker compose exec -T db pg_dump \
  -U gis_user \
  -d parcel_db \
  -Fc \
  > "backups/parcel_db_$(date +%Y%m%d_%H%M%S).dump"