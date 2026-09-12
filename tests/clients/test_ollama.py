"""Unit tests for the isolated Ollama HTTP client."""

import json

import httpx2
import pytest

from app.clients.ollama import OllamaClient
from app.core.exceptions import (
    OllamaConnectionError,
    OllamaResponseError,
    OllamaTimeoutError,
)


def build_client(handler):
    """Build an Ollama client backed by an in-memory HTTP transport."""
    return OllamaClient(
        base_url="http://ollama.test",
        model="qwen2.5-coder:14b",
        timeout=1,
        transport=httpx2.MockTransport(handler),
    )


@pytest.mark.asyncio
async def test_generate_text_posts_configured_model_and_prompt():
    """Verify that generation uses the configured Ollama contract."""
    received_request = None

    def handler(request: httpx2.Request) -> httpx2.Response:
        nonlocal received_request
        received_request = request
        return httpx2.Response(200, json={"response": "Generated analysis"})

    response = await build_client(handler).generate_text("Investigate DNS failure")

    assert response == "Generated analysis"
    assert received_request is not None
    assert received_request.url == "http://ollama.test/api/generate"
    assert json.loads(received_request.content) == {
        "model": "qwen2.5-coder:14b",
        "prompt": "Investigate DNS failure",
        "stream": False,
    }


@pytest.mark.asyncio
async def test_generate_text_maps_timeout_to_controlled_error():
    """Verify that an HTTP timeout does not leak from the client boundary."""

    def handler(request: httpx2.Request) -> httpx2.Response:
        raise httpx2.ReadTimeout("timed out", request=request)

    with pytest.raises(OllamaTimeoutError):
        await build_client(handler).generate_text("Test prompt")


@pytest.mark.asyncio
async def test_generate_text_maps_connection_failure_to_controlled_error():
    """Verify that a connection failure does not leak from the client boundary."""

    def handler(request: httpx2.Request) -> httpx2.Response:
        raise httpx2.ConnectError("connection refused", request=request)

    with pytest.raises(OllamaConnectionError):
        await build_client(handler).generate_text("Test prompt")


@pytest.mark.asyncio
async def test_generate_text_maps_invalid_response_to_controlled_error():
    """Verify that malformed provider output is rejected predictably."""

    def handler(_request: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(200, json={"unexpected": "payload"})

    with pytest.raises(OllamaResponseError):
        await build_client(handler).generate_text("Test prompt")


@pytest.mark.asyncio
async def test_generate_text_maps_provider_http_error_to_controlled_error():
    """Verify that provider HTTP failures are normalized by the client."""

    def handler(_request: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(503, json={"error": "unavailable"})

    with pytest.raises(OllamaResponseError):
        await build_client(handler).generate_text("Test prompt")
