from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Secrets and runtime settings are loaded from environment/.env, never committed."""
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    ai_api_key: str | None = None
    ai_base_url: str = "https://api.openai.com/v1"
    ai_model: str = "gpt-4o-mini"
    assistant_name: str = "J-A-R-V-I-S"
    request_timeout_seconds: float = 45.0

settings = Settings()
