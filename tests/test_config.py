from app.core.config import settings


def test_settings_defaults():
    assert settings.app_env == "development"
    assert settings.ollama_base_url == "http://localhost:11434"
    assert settings.ollama_model == "qwen2.5-coder:14b"
    assert settings.ollama_timeout == 60
