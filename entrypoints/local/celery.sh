#!/bin/sh

export PYTHONPATH=$(pwd)

echo "Starting Celery Worker..."

exec python -m celery -A celery_app worker \
  --loglevel=INFO \
  --concurrency=2 \
  --prefetch-multiplier=1