import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from google.adk.runners import InMemoryRunner
from google.genai import types
from agent import root_agent

app = FastAPI(
    title="ADK Agent on Cloud Run",
    description="Enterprise API to invoke a custom google-adk agent.",
    version="1.0.0"
)

# Instantiate the Runner
app_name = "adk-cloudrun-demo"
runner = InMemoryRunner(agent=root_agent, app_name=app_name)

class InvokeRequest(BaseModel):
    prompt: str
    user_id: str = "default_user"

class InvokeResponse(BaseModel):
    response: str
    session_id: str

@app.get("/health")
def health():
    return {"status": "healthy", "agent": root_agent.name}

@app.post("/invoke", response_model=InvokeResponse)
async def invoke(request: InvokeRequest):
    try:
        # Create a new session for this interaction
        session = await runner.session_service.create_session(
            app_name=runner.app_name, user_id=request.user_id
        )
        
        # Convert prompt into Content structure
        content = types.Content(parts=[types.Part(text=request.prompt)])
        
        response_text = ""
        # Run the runner asynchronously
        async for event in runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=content,
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        response_text += part.text
        
        if not response_text:
            raise HTTPException(status_code=500, detail="Agent did not produce a response.")
            
        return InvokeResponse(
            response=response_text,
            session_id=session.id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
