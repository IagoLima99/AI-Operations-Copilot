"""FastAPI dependency providers for chat components."""

from typing import Annotated

from fastapi import Depends

from app.clients.ollama import OllamaClient
from app.services.chat_service import ChatService


def get_ollama_client() -> OllamaClient:
    """Create an Ollama client instance."""
    return OllamaClient()


def get_chat_service(
    ollama_client: Annotated[
        OllamaClient,
        Depends(get_ollama_client),
    ],
) -> ChatService:
    """Create a chat service with its Ollama client dependency."""
    return ChatService(ollama_client)
