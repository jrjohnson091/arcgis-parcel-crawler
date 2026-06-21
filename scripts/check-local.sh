#!/usr/bin/env bash
set -euxo pipefail

PROJECT_NAME="${COMPOSE_PROJECT_NAME:-parcel-dev}"

if [ $(uname -s) = "Linux" ]; then
    echo "Remove __pycache__ files"
    sudo find . -type d -name __pycache__ -exec rm -r {} \+
fi

docker -p "$PROJECT_NAME" compose build
docker -p "$PROJECT_NAME" compose up -d backend
docker -p "$PROJECT_NAME" compose exec -T backend bash scripts/check.sh