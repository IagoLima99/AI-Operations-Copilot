"""Configure the FastAPI application and its exception handlers."""

from fastapi import FastAPI

from app.api.exception_handlers import (
    ollama_exception_connection_handler,
    ollama_exception_response_handler,
    ollama_exception_timeout_handler,
)
from app.api.router import router
from app.core.exceptions import (
    OllamaConnectionError,
    OllamaResponseError,
    OllamaTimeoutError,
)

app = FastAPI()
app.include_router(router)

app.add_exception_handler(OllamaTimeoutError, ollama_exception_timeout_handler)
app.add_exception_handler(OllamaConnectionError, ollama_exception_connection_handler)
app.add_exception_handler(OllamaResponseError, ollama_exception_response_handler)
