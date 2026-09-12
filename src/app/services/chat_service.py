"""Application service for chat requests."""

from app.clients.ollama import OllamaClient


class ChatService:
    """Coordinate chat response generation."""

    def __init__(self, ollama_client: OllamaClient):
        """Initialize the service with an Ollama client."""

        self.ollama_client = ollama_client

    async def get_chat_response(self, prompt: str) -> str:
        """Generate a chat response for the provided prompt."""
        return await self.ollama_client.generate_text(prompt)
        # raise OllamaTimeoutError("Test timeout") teste para debug
