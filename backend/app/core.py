"""Conversation core and provider integration."""
from uuid import uuid4
from .providers import get_provider

_sessions: dict[str, list[dict[str, str]]] = {}
SYSTEM_PROMPT = """You are J-A-R-V-I-S, a helpful personal AI assistant.
Be clear, capable, concise by default, and honest about limitations.
Do not claim actions were completed unless they actually were."""

async def respond(message: str, conversation_id: str | None = None) -> dict[str, str]:
    session_id = conversation_id or str(uuid4())
    history = _sessions.setdefault(session_id, [])
    history.append({"role": "user", "content": message.strip()})
    provider = get_provider()
    if provider is None:
        reply = "Message received and saved in this session. The AI provider is not configured yet. Set AI_API_KEY in the backend environment to enable model responses."
        mode = "provider_not_configured"
    else:
        try:
            reply = await provider.generate([{"role": "system", "content": SYSTEM_PROMPT}, *history])
            mode = "ai"
        except Exception as exc:
            reply = f"I couldn't reach the configured AI provider. Please check your provider settings. ({type(exc).__name__})"
            mode = "provider_error"
    history.append({"role": "assistant", "content": reply})
    return {"conversation_id": session_id, "reply": reply, "mode": mode}

def get_history(conversation_id: str) -> list[dict[str, str]]:
    return list(_sessions.get(conversation_id, []))

def clear_history(conversation_id: str) -> bool:
    return _sessions.pop(conversation_id, None) is not None
