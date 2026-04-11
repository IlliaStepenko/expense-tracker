#!/bin/sh

export PYTHONPATH=$(pwd)

echo "Starting Celery Worker..."

exec celery -A celery worker \
  --loglevel=INFO \
  --concurrency=2 \
  --prefetch-multiplier=1