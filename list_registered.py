import vertexai
from vertexai import agent_engines

vertexai.init(project="warier-agents", location="us-central1")

print("Listing registered reasoning engines (Agents)...")
engines = list(agent_engines.list())
print(f"Found {len(engines)} reasoning engine(s):")
for engine in engines:
    print(f"- {engine.display_name}: {engine.resource_name}")
