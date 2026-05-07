import vertexai
from google.cloud import aiplatform

vertexai.init(project="warier-agents", location="us-east1")

print("Listing Vertex AI Experiments...")
experiments = aiplatform.Experiment.list()
print(f"Found {len(experiments)} experiment(s):")
for exp in experiments:
    print(f"- {exp.name}")
