"""
AI Web Builder Agent - Web Server
FastAPI server that connects the frontend UI with the Python agent
"""

import os
from typing import Optional
from pathlib import Path


from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from main import AIWebAgent


# Initialize FastAPI app
app = FastAPI(
    title="AI Web Builder Agent",
    description="AI-powered web development agent that generates HTML websites",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the agent
agent = AIWebAgent(api_key=os.getenv("OPENAI_API_KEY"))


# Pydantic models for request/response
class MessageRequest(BaseModel):
    """Request model for chat messages"""

    message: str
    api_key: Optional[str] = None


class APIKeyRequest(BaseModel):
    """Request model for setting API key"""

    api_key: str


class ClearHistoryRequest(BaseModel):
    """Request model for clearing conversation history"""

    confirm: bool = False


@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """
    Serve the frontend HTML file
    """
    # Get the path to index.html (parent directory of agent folder)
    parent_dir = Path(__file__).parent.parent
    index_path = parent_dir / "index.html"

    if not index_path.exists():
        raise HTTPException(status_code=404, detail="index.html not found")

    with open(index_path, "r", encoding="utf-8") as f:
        return f.read()


@app.post("/api/chat")
async def chat(request: MessageRequest):
    """
    Process a user message and generate website code

    Args:
        request: MessageRequest containing the user message and optional API key

    Returns:
        JSON response with generated code and explanation
    """
    # Update API key if provided
    if request.api_key:
        agent.set_api_key(request.api_key)

    # Check if API key is set
    if not agent.api_key:
        return JSONResponse(
            status_code=400,
            content={
                "error": "API key not set. Please provide an API key.",
                "code": "",
                "explanation": "",
            },
        )

    # Generate website
    result = await agent.generate_website(request.message)

    if result["error"]:
        return JSONResponse(status_code=500, content=result)

    return JSONResponse(
        content={
            "code": result["code"],
            "explanation": result["explanation"],
            "error": None,
        }
    )


@app.get("/api/history")
async def get_history():
    """
    Get the conversation history

    Returns:
        JSON response with conversation history
    """
    return {
        "history": agent.get_conversation_history(),
        "has_code": bool(agent.generated_code),
    }


@app.post("/api/clear")
async def clear_history(request: ClearHistoryRequest):
    """
    Clear the conversation history

    Args:
        request: ClearHistoryRequest with confirmation

    Returns:
        JSON response confirming the action
    """
    if request.confirm:
        agent.clear_history()
        return {"message": "History cleared successfully"}
    else:
        return JSONResponse(
            status_code=400,
            content={"error": "Please set confirm=true to clear history"},
        )


@app.post("/api/download")
async def download_code():
    """
    Get the generated code for download

    Returns:
        JSON response with the generated code
    """
    if not agent.generated_code:
        return JSONResponse(status_code=400, content={"error": "No code generated yet"})

    return {"code": agent.generated_code, "filename": "generated-website.html"}


@app.get("/api/status")
async def get_status():
    """
    Get the current status of the agent

    Returns:
        JSON response with agent status
    """
    return {
        "has_api_key": bool(agent.api_key),
        "has_generated_code": bool(agent.generated_code),
        "conversation_length": len(agent.conversation_history),
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler
    """
    return JSONResponse(
        status_code=500, content={"error": f"Internal server error: {str(exc)}"}
    )


def main():
    """
    Run the server
    """
    # Get configuration from environment variables
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("RELOAD", "false").lower() == "true"

    print(f"Starting AI Web Builder Agent server...")
    print(f"Frontend: http://{host}:{port}")
    print(f"API Documentation: http://{host}:{port}/docs")

    # Run the server
    uvicorn.run("agent.server:app", host=host, port=port, reload=reload)


if __name__ == "__main__":
    main()
