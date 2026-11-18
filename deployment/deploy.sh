#!/bin/bash
set -e

PROJECT_DIR="/home/umar/secure-api-infrastructure"
SERVICE_NAME="secure-api"

echo "Starting deployment..."

cd "$PROJECT_DIR"

echo "Pulling latest code..."
git pull origin main

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running tests..."
pytest -v

echo "Restarting API service..."
sudo systemctl restart "$SERVICE_NAME"

echo "Checking service status..."
sudo systemctl is-active "$SERVICE_NAME"

echo "Deployment completed successfully!"
