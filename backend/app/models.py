from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=20_000)
    conversation_id: str | None = None

class ChatResponse(BaseModel):
    conversation_id: str
    reply: str
    mode: str
    provider_configured: bool
