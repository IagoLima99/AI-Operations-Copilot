"""Tests for the chat application service."""

import pytest

from app.services.chat_service import ChatService


class FakeOllamaClient:
    """Provide a deterministic Ollama client test double."""

    def __init__(self):
        """Initialize the received prompt tracker."""
        self.received_prompt = None

    async def generate_text(self, prompt: str) -> str:
        """Record the prompt and return a deterministic response."""
        self.received_prompt = prompt
        return "DNS lookup for example.com"


@pytest.mark.asyncio
async def test_chat_service():
    """Verify that the service forwards prompts to its client."""
    fake_client = FakeOllamaClient()
    chat_service = ChatService(fake_client)
    response = await chat_service.get_chat_response("Test prompt")
    assert response == "DNS lookup for example.com"
    assert fake_client.received_prompt == "Test prompt"
