"""Tests for application configuration defaults."""

from app.core.config import settings


def test_settings_defaults():
    """Verify the default settings values."""
    assert settings.app_env == "development"
    assert settings.ollama_base_url == "http://localhost:11434"
    assert settings.ollama_model == "qwen2.5-coder:14b"
    assert settings.ollama_timeout == 60
