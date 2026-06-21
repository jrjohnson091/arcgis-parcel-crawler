#!/usr/bin/env bash
set -euxo pipefail

cleanup() {
  ./scripts/dc-test down -v --remove-orphans
}

trap cleanup EXIT

echo "Removing __pycache__ directories..."
find . -type d -name __pycache__ -prune -exec rm -rf {} +

./scripts/dc-test down -v --remove-orphans
./scripts/dc-test build
./scripts/dc-test up -d db
./scripts/dc-test run --rm prestart
./scripts/dc-test run --rm backend bash scripts/tests-start.sh