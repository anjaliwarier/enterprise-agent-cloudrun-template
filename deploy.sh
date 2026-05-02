#!/bin/bash

# Exit on error
set -e

# Load configurations from .env file
if [ -f .env ]; then
    export $(cat .env | grep -v '#' | xargs)
else
    echo "ERROR: .env file not found. Please copy .env.example to .env and configure it."
    exit 1
fi

PROJECT_ID="${GOOGLE_CLOUD_PROJECT}"
REGION="${GOOGLE_CLOUD_LOCATION}"
SERVICE_NAME="adk-cloudrun-demo"
IMAGE_TAG="${REGION}-docker.pkg.dev/${PROJECT_ID}/adk-agents-repo/${SERVICE_NAME}:latest"

echo "============================================================"
echo "1. Packaging and building ADK Agent on Google Cloud Build..."
echo "============================================================"
gcloud builds submit --tag "${IMAGE_TAG}" .

echo "============================================================"
echo "2. Deploying ADK Agent to Google Cloud Run..."
echo "============================================================"
gcloud run deploy "${SERVICE_NAME}" \
    --image "${IMAGE_TAG}" \
    --region "${REGION}" \
    --platform managed \
    --allow-unauthenticated \
    --set-env-vars "GOOGLE_CLOUD_PROJECT=${PROJECT_ID}"

echo "============================================================"
echo "3. Registering Agent in Vertex AI Agent Registry..."
echo "============================================================"
python register_agent.py

echo "============================================================"
echo "🚀 ADK Agent successfully deployed on Cloud Run and registered in the Agent Registry!"
echo "============================================================"
