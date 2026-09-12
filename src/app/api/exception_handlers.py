"""HTTP exception handlers for Ollama integration failures."""

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette import status

from app.core.exceptions import (
    OllamaConnectionError,
    OllamaResponseError,
    OllamaTimeoutError,
)


async def ollama_exception_timeout_handler(
    _request: Request, _exc: OllamaTimeoutError
) -> JSONResponse:
    """Return a service-unavailable response for Ollama timeouts."""
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": "AI service is temporarily unavailable"},
    )


async def ollama_exception_connection_handler(
    _request: Request, _exc: OllamaConnectionError
) -> JSONResponse:
    """Return a service-unavailable response for Ollama connection errors."""
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": "Unable to connect to AI service"},
    )


async def ollama_exception_response_handler(
    _request: Request, _exc: OllamaResponseError
) -> JSONResponse:
    """Return a bad-gateway response for invalid Ollama responses."""
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={"detail": "AI service is not responding"},
    )
