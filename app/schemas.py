from pydantic import BaseModel, Field


class ChatRequest(BaseModel):

    session_id: str = Field(
        ...,
        description="Unique conversation session ID"
    )

    message: str = Field(
        ...,
        description="Patient message"
    )


class ChatResponse(BaseModel):

    session_id: str

    response: str

    tool_trace: list = []

