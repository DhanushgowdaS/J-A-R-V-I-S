"""Provider boundary for OpenAI-compatible chat completion APIs."""
from typing import Protocol
import httpx
from .config import settings

class AIProvider(Protocol):
    async def generate(self, messages: list[dict[str, str]]) -> str: ...

class OpenAICompatibleProvider:
    def __init__(self, api_key: str, base_url: str, model: str, timeout: float = 45.0):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    async def generate(self, messages: list[dict[str, str]]) -> str:
        endpoint = f"{self.base_url}/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"model": self.model, "messages": messages}
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(endpoint, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
        try:
            return str(data["choices"][0]["message"]["content"]).strip()
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError("AI provider returned an unexpected response format") from exc

def get_provider() -> AIProvider | None:
    if not settings.ai_api_key:
        return None
    return OpenAICompatibleProvider(
        api_key=settings.ai_api_key,
        base_url=settings.ai_base_url,
        model=settings.ai_model,
        timeout=settings.request_timeout_seconds,
    )
