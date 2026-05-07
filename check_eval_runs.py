import os
import vertexai
from google.cloud import aiplatform
from google import genai

# Initialize Vertex AI
vertexai.init(project="warier-agents", location="us-central1")

print("============================================================")
print("Checking programmatically for completed Evaluation Runs...")
print("============================================================")

try:
    # 1. Try using google-genai client
    client = genai.Client(vertexai=True, project="warier-agents", location="us-central1")
    print("\nChecking via google-genai client...")
    # GenAI SDK list evaluation runs
    runs = list(client.evals.list_evaluation_runs())
    print(f"Found {len(runs)} evaluation run(s) in GenAI Registry:")
    for run in runs:
        print(f"- Run Name: {run.name}")
        print(f"  State: {run.state}")
        print(f"  Create Time: {run.create_time}\n")
except Exception as e:
    print(f"GenAI SDK check returned: {e}")

try:
    # 2. Try listing via aiplatform Experiments
    print("\nChecking via aiplatform Experiments...")
    experiments = aiplatform.Experiment.list()
    for exp in experiments:
        runs = aiplatform.ExperimentRun.list(experiment=exp.name)
        if runs:
            print(f"Experiment: {exp.name} (Found {len(runs)} run(s)):")
            for run in runs:
                print(f"- Run Name: {run.name}")
except Exception as e:
    print(f"aiplatform Experiments check returned: {e}")
