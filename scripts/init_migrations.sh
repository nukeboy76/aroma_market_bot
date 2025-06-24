#!/usr/bin/env bash
set -euo pipefail

alembic init -t async alembic
alembic revision --autogenerate -m "initial"
alembic upgrade head

set -o allexport
source .env
set +o allexport

psql \
  -v ON_ERROR_STOP=1 \
  "postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${DB_HOST}:${DB_PORT}/${POSTGRES_DB}" \
  -f scripts/seed_data.sql
