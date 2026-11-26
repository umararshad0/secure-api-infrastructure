#!/bin/bash
set -Eeuo pipefail

PROJECT_DIR="/home/umar/secure-api-infrastructure"
SERVICE_NAME="secure-api"
HEALTHCHECK_URL="${HEALTHCHECK_URL:-http://127.0.0.1:8000/}"

echo "Starting deployment..."

cd "$PROJECT_DIR"

echo "Pulling latest code..."
git pull origin main

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running tests..."
python -m pytest -v

echo "Restarting API service..."
sudo systemctl restart "$SERVICE_NAME"

echo "Checking service status..."
sudo systemctl is-active "$SERVICE_NAME"

echo "Checking API health at $HEALTHCHECK_URL..."
if ! HTTP_STATUS=$(curl \
    --fail \
    --silent \
    --show-error \
    --retry 5 \
    --retry-connrefused \
    --retry-delay 2 \
    --connect-timeout 2 \
    --max-time 5 \
    --output /dev/null \
    --write-out '%{http_code}' \
    "$HEALTHCHECK_URL"); then
    echo "API health check request failed." >&2
    exit 1
fi

if [[ ! "$HTTP_STATUS" =~ ^2[0-9]{2}$ ]]; then
    echo "API health check returned HTTP $HTTP_STATUS; expected a 2xx response." >&2
    exit 1
fi

echo "Deployment completed successfully!"
