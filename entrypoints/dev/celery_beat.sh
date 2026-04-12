#!/bin/sh

set -e

export PYTHONPATH=$(pwd)

echo "Starting Celery Beat..."

exec python -m celery -A celery_app beat \
    --loglevel=INFO \
    --max-interval=30