"""Chat generation API route."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import get_chat_service
from app.schemas.ai_request_chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter()


@router.post("", response_model=ChatResponse)
async def chat_endpoint(
    chat_request: ChatRequest,
    chat_service: Annotated[
        ChatService,
        Depends(get_chat_service),
    ],
):
    """Generate a chat response from the submitted prompt."""
    return ChatResponse(
        response=await chat_service.get_chat_response(chat_request.prompt)
    )
