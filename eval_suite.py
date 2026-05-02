import asyncio
import os
import pathlib
from dotenv import load_dotenv
from google.adk.evaluation.agent_evaluator import AgentEvaluator

# Load environment variables
load_dotenv()

async def run_evaluation():
    print("============================================================")
    echo = "1. Starting programmatical evaluation using Vertex AI / Gemini Enterprise features..."
    print(echo)
    print("============================================================")
    
    # Path to our mock evaluation dataset
    dataset_path = str(pathlib.Path(__file__).parent / "eval_data")
    
    # Run the native evaluator
    await AgentEvaluator.evaluate(
        agent_module="agent",  # This points to agent.py
        eval_dataset_file_path_or_dir=dataset_path,
        num_runs=1,
    )
    
    print("============================================================")
    print("✅ Programmatical Evaluation suite completed successfully!")
    print("============================================================")

if __name__ == "__main__":
    asyncio.run(run_evaluation())
