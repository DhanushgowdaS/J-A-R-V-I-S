"""Conversation core with persistent history and provider integration."""
from uuid import uuid4
from . import database
from .providers import get_provider

SYSTEM_PROMPT = """You are J-A-R-V-I-S, a helpful personal AI assistant.
Be clear, capable, concise by default, and honest about limitations.
Do not claim actions were completed unless they actually were."""

async def respond(message: str, conversation_id: str | None = None) -> dict[str, str]:
    session_id = conversation_id or str(uuid4())
    database.create_conversation(session_id)
    database.add_message(session_id,"user",message.strip())
    history = database.history(session_id)
    memories = database.list_memories(limit=30)
    memory_context = ""
    if memories:
        memory_context = "\n\nStored user memories (use only when relevant):\n" + "\n".join(f"- {m['content']}" for m in memories)
    provider = get_provider()
    if provider is None:
        reply = "Message received and saved. The AI provider is not configured yet. Set AI_API_KEY in the backend environment to enable model responses."
        mode = "provider_not_configured"
    else:
        try:
            reply = await provider.generate([{"role":"system","content":SYSTEM_PROMPT + memory_context},*history])
            mode = "ai"
        except Exception as exc:
            reply = f"I couldn't reach the configured AI provider. Please check provider settings. ({type(exc).__name__})"
            mode = "provider_error"
    database.add_message(session_id,"assistant",reply)
    return {"conversation_id":session_id,"reply":reply,"mode":mode}

def get_history(conversation_id: str):
    return database.history(conversation_id)

def list_history():
    return database.list_conversations()

def clear_history(conversation_id: str) -> bool:
    return database.delete_conversation(conversation_id)
