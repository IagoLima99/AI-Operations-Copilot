"""Request and response schemas for chat operations."""

from pydantic import BaseModel


class ChatRequest(BaseModel):
    """Represent a chat generation request."""

    prompt: str


class ChatResponse(BaseModel):
    """Represent a generated chat response."""

    response: str
