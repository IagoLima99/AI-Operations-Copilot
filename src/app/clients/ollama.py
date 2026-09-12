"""Asynchronous client for the Ollama generation API."""

import json

import httpx2

from app.core.config import settings
from app.core.exceptions import (
    OllamaConnectionError,
    OllamaResponseError,
    OllamaTimeoutError,
)


class OllamaClient:
    """Generate text through the configured Ollama service."""

    def __init__(
        self,
        *,
        base_url: str | None = None,
        model: str | None = None,
        timeout: float | None = None,
        transport: httpx2.AsyncBaseTransport | None = None,
    ):
        """Initialize the client with settings or explicitly injected values.

        The optional transport provides an isolated HTTP seam for tests without
        changing the production request path.
        """
        self.ollama_base_url = (
            settings.ollama_base_url if base_url is None else base_url
        )
        self.ollama_model = settings.ollama_model if model is None else model
        self.ollama_timeout = settings.ollama_timeout if timeout is None else timeout
        self._transport = transport

    async def generate_text(self, prompt: str) -> str:
        """Return generated text for the provided prompt."""

        url = f"{self.ollama_base_url}/api/generate"
        payload = {
            "model": self.ollama_model,
            "prompt": prompt,
            "stream": False,
        }

        async with httpx2.AsyncClient(
            timeout=self.ollama_timeout,
            transport=self._transport,
        ) as client:
            try:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
                if not isinstance(data, dict):
                    raise OllamaResponseError("Ollama response must be a JSON object")
                generated_text = data["response"]
                if not isinstance(generated_text, str):
                    raise OllamaResponseError(
                        "Ollama response field 'response' must be a string"
                    )
                return generated_text
            except httpx2.TimeoutException as e:
                raise OllamaTimeoutError("Ollama request timed out") from e
            except httpx2.RequestError as e:
                raise OllamaConnectionError("Unable to connect to Ollama") from e
            except httpx2.HTTPStatusError as e:
                raise OllamaResponseError(
                    f"Ollama returned HTTP {e.response.status_code}"
                ) from e
            except json.JSONDecodeError as e:
                raise OllamaResponseError(
                    "Ollama returned an invalid JSON response"
                ) from e
            except KeyError as e:
                raise OllamaResponseError(
                    "Ollama response is missing the expected 'response' field"
                ) from e
