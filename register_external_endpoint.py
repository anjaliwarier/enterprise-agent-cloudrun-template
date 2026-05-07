import os
import sys
import logging
import requests
import google.auth
from google.auth.transport.requests import Request
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "YOUR_GCP_PROJECT_ID")
REGION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
SERVICE_NAME = "adk-cloudrun-demo"
CLOUD_RUN_URL = f"https://{SERVICE_NAME}-376660136590.{REGION}.run.app"

logger.info(f"Registering External Cloud Run Endpoint: {CLOUD_RUN_URL} inside the Agent Registry...")

try:
    # Obtain default credentials
    credentials, project = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    auth_req = Request()
    credentials.refresh(auth_req)
    bearer_token = credentials.token

    # Define endpoint details
    url = f"https://{REGION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{REGION}/endpoints"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "displayName": "adk_cloudrun_risk_analyst",
        "description": "Pre-deployed Cloud Run containerized ADK Agent Endpoint",
        "labels": {
            "deployed_on": "cloud_run",
            "runtime": "fastapi"
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code in [200, 201]:
        endpoint_data = response.json()
        # If LRO is returned, extract it
        if "name" in endpoint_data:
            logger.info(f"Successfully registered external endpoint in the Agent Registry! Resource ID: {endpoint_data['name']}")
        else:
            logger.info("Endpoint created successfully.")
    else:
        logger.error(f"Failed to register endpoint. Status Code: {response.status_code}, Error: {response.text}")
        sys.exit(1)

except Exception as e:
    logger.error(f"An unexpected error occurred during registration: {e}")
    sys.exit(1)
