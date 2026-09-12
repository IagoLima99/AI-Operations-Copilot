"""Tests for the chat API route and provider failure mappings."""

import json

import pytest
from starlette.requests import Request

from app.api.exception_handlers import (
    ollama_exception_connection_handler,
    ollama_exception_response_handler,
    ollama_exception_timeout_handler,
)
from app.api.routes.chat import chat_endpoint
from app.core.exceptions import (
    OllamaConnectionError,
    OllamaResponseError,
    OllamaTimeoutError,
)
from app.schemas.ai_request_chat import ChatRequest


class FakeChatService:
    """Provide a deterministic chat service test double."""

    async def get_chat_response(self, prompt: str) -> str:
        """Return a deterministic chat response."""
        return "DNS lookup for example.com"


@pytest.mark.asyncio
async def test_chat_endpoint():
    """Verify that the route returns the isolated service response."""
    response = await chat_endpoint(
        ChatRequest(prompt="Test prompt"),
        FakeChatService(),
    )

    assert response.model_dump() == {"response": "DNS lookup for example.com"}


@pytest.mark.parametrize(
    ("handler", "provider_error", "expected_status", "expected_detail"),
    [
        (
            ollama_exception_timeout_handler,
            OllamaTimeoutError("request timed out"),
            503,
            "AI service is temporarily unavailable",
        ),
        (
            ollama_exception_connection_handler,
            OllamaConnectionError("connection refused"),
            503,
            "Unable to connect to AI service",
        ),
        (
            ollama_exception_response_handler,
            OllamaResponseError("invalid response"),
            502,
            "AI service is not responding",
        ),
    ],
)
@pytest.mark.asyncio
async def test_provider_error_handler(
    handler,
    provider_error: Exception,
    expected_status: int,
    expected_detail: str,
):
    """Verify that provider failures are mapped without leaking internals."""
    request = Request(
        {
            "type": "http",
            "method": "POST",
            "path": "/chat",
            "headers": [],
        }
    )

    response = await handler(request, provider_error)

    assert response.status_code == expected_status
    assert json.loads(response.body) == {"detail": expected_detail}
