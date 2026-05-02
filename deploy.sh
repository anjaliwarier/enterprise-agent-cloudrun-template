#!/bin/bash

# Exit on error
set -e

# Variables
PROJECT_ID="warier-agents"
REGION="us-central1"
SERVICE_NAME="adk-cloudrun-demo"
IMAGE_TAG="us-central1-docker.pkg.dev/${PROJECT_ID}/adk-agents-repo/${SERVICE_NAME}:latest"

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
