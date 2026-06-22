#!/usr/bin/env bash
set -euxo pipefail

PROJECT_NAME="${COMPOSE_PROJECT_NAME:-parcel-dev}"

git clean -fdX

docker -p "$PROJECT_NAME" compose build
docker -p "$PROJECT_NAME" compose up -d backend
docker -p "$PROJECT_NAME" compose exec -T backend bash scripts/check.sh