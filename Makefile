.PHONY: help up down restart build shell logs db psql notebook \
        clean test test-up test-down test-shell test-logs

help:
	@echo "Available targets:"
	@echo "  make up          - Start development services"
	@echo "  make down        - Stop development services"
	@echo "  make restart     - Restart development services"
	@echo "  make build       - Rebuild images"
	@echo "  make shell       - Open backend shell"
	@echo "  make logs        - Follow backend logs"
	@echo "  make db          - Open psql in database container"
	@echo "  make notebook    - Start notebook service"
	@echo "  make test        - Run integration tests"
	@echo "  make clean       - Remove __pycache__ directories"

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose down
	docker compose up -d

build:
	docker compose build

shell:
	docker compose exec backend bash

be-logs:
	docker compose logs -f backend

nb-logs:
	docker compose logs -f notebook

db-logs:
	docker compose logs -f db

db:
	docker compose exec db psql -U gis_user -d parcel_db

psql: db

notebook:
	docker compose up -d notebook

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +

test:
	./scripts/test-local.sh

test-up:
	./scripts/dc-test up -d

test-down:
	./scripts/dc-test down -v --remove-orphans

test-shell:
	./scripts/dc-test exec backend bash

test-logs:
	./scripts/dc-test logs -f backend