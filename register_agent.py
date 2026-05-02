import os
import sys
import vertexai
import logging
from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from google.genai import types

# Load env variables
load_dotenv()

# Official imports for Vertex AI Reasoning Engines Agent Registry
from vertexai import agent_engines
from vertexai.preview.reasoning_engines import AdkApp
from agent import root_agent

# Configure logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PROJECT_ID = "warier-agents"
REGION = "us-central1"

# Initialize Vertex AI
vertexai.init(
    project=PROJECT_ID,
    location=REGION,
    staging_bucket="gs://warier-agents",
)

logger.info("Registering ADK Agent in the Vertex AI Agent Registry...")

# Create the Reasoning Engine Application
app = AdkApp(
    agent=root_agent,
    enable_tracing=True,
)

# Register and deploy as a Reasoning Engine instance
remote_app = agent_engines.create(
    app,
    display_name="adk_cloudrun_risk_analyst",
    requirements=[
        "google-cloud-aiplatform[adk,agent-engines]>=1.100.0,<2.0.0",
        "google-adk>=1.5.0,<2.0.0",
        "python-dotenv",
        "google-cloud-secret-manager"
    ],
)

logger.info(f"Successfully registered agent in Agent Registry! Resource Name: {remote_app.resource_name}")
