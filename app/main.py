from fastapi import FastAPI

from app.agent import run_agent
from app.schemas import ChatRequest, ChatResponse


app = FastAPI(
    title="Self-Improving Appointment Agent",
    description="AI appointment scheduling agent with evaluation and self-improvement",
    version="1.0.0"
)


@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "message": "Appointment Agent API is running"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    result = run_agent(
        session_id=request.session_id,
        user_message=request.message
    )

    return ChatResponse(
        session_id=request.session_id,
        response=result["response"],
        tool_trace=result["tool_trace"]
    )
