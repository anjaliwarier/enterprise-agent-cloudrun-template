import os
import sys
import logging
import asyncio
from dotenv import load_dotenv

# Load configurations from .env file
load_dotenv()

from google import genai
from google.genai import types

# Configure logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "YOUR_GCP_PROJECT_ID")
REGION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
STAGING_BUCKET = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")
ENDPOINT_ID = "1197122421799256064"  # Your registered Endpoint Resource ID

if STAGING_BUCKET and not STAGING_BUCKET.startswith("gs://"):
    STAGING_BUCKET = f"gs://{STAGING_BUCKET}"

# Define agent prompts for evaluation
agent_prompts = [
    "What are the main property insurance operational risks in coastal zones?",
    "What are the primary operational risks for P&C insurers during hurricanes?",
    "How does catastrophe modeling help insurers manage property risk?",
    "What strategic recommendations do you have for P&C insurance underwriters?"
]

async def run_evaluation():
    logger.info("============================================================")
    logger.info("1. Programmatically running Gen AI Evaluations via SDK...")
    logger.info("============================================================")
    
    try:
        # Initialize the Vertex AI GenAI Client
        client = genai.Client(
            vertexai=True,
            project=PROJECT_ID,
            location=REGION
        )

        # Define dataset structure
        session_inputs = types.evals.SessionInput(user_id="eval_user", state={})
        
        # Format dataset
        import pandas as pd
        agent_dataset = pd.DataFrame({
            "prompt": agent_prompts,
            "session_inputs": [session_inputs] * len(agent_prompts)
        })

        AGENT = f"projects/{PROJECT_ID}/locations/{REGION}/endpoints/{ENDPOINT_ID}"

        # Define agent info for metadata
        google_search = types.FunctionDeclaration(
            description="Search Google for web results and factual information.",
            name="google_search",
            parameters={
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
                "type": "object",
            },
        )
        agent_info = types.evals.AgentInfo(
            agents={
                "adk_cloudrun_risk_analyst": types.evals.AgentConfig(
                    agent_id="adk_cloudrun_risk_analyst",
                    instruction="You are an expert Risk Analyst Agent. You have access to Google Search.",
                    tools=[types.Tool(function_declarations=[google_search])],
                )
            },
            root_agent_id="adk_cloudrun_risk_analyst",
        )

        # Trigger managed evaluation run
        evaluation_run = client.evals.create_evaluation_run(
            dataset=agent_dataset,
            agent=AGENT,
            agent_info=agent_info,
            metrics=[
                types.RubricMetric.FINAL_RESPONSE_QUALITY,
                types.RubricMetric.TOOL_USE_QUALITY,
                types.RubricMetric.HALLUCINATION,
                types.RubricMetric.SAFETY
            ],
            dest=STAGING_BUCKET
        )

        logger.info(f"Managed Evaluation Run started successfully! Status: {evaluation_run.status}")
        logger.info(f"Run ID: {evaluation_run.name}")
        logger.info("============================================================")
        logger.info("✅ Metrics are now calculating in the background on Vertex AI!")
        logger.info("============================================================")

    except Exception as e:
        logger.error(f"Failed to run programmatic evaluation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(run_evaluation())
