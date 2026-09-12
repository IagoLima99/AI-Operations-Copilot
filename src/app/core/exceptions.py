"""Domain exceptions raised by the Ollama integration."""


class OllamaError(Exception):
    """Base exception for Ollama integration failures."""

    pass


class OllamaTimeoutError(OllamaError):
    """Raised when an Ollama request exceeds its timeout."""

    pass


class OllamaConnectionError(OllamaError):
    """Raised when a connection to Ollama cannot be established."""

    pass


class OllamaResponseError(OllamaError):
    """Raised when Ollama returns an invalid or unsuccessful response."""

    pass
