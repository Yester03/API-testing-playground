#!/usr/bin/env bash
set -e

mkdir -p data uploads

if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

HOST=${APP_HOST:-0.0.0.0}
PORT=${APP_PORT:-8000}

uvicorn app.main:app --host "$HOST" --port "$PORT"
