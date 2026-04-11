#!/bin/sh

set -e

echo "Starting Celery Beat ..."

exec celery -A celery beat \
  --loglevel=INFO \
  --max-interval=30