#!/usr/bin/env bash
set -euo pipefail

backup_file="${1:?Usage: scripts/restore_db.sh backups/file.dump}"

docker compose exec -T db pg_restore \
  -U gis_user \
  -d parcel_db \
  --clean \
  --if-exists \
  < "$backup_file"