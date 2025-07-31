#!/usr/bin/env bash

set -e

echo "Run apply megrations..."
alembic upgrade head
echo "Megrations applied"

exec "$@"