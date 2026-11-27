from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_chat_creates_session_and_returns_provider_status():
    response = client.post("/api/chat", json={"message": "Hello JARVIS"})
    assert response.status_code == 200
    data = response.json()
    assert data["conversation_id"]
    assert data["reply"]
    assert data["mode"] in ("provider_not_configured", "ai", "provider_error")
    assert "provider_configured" in data

def test_chat_reuses_conversation_id_and_history():
    first = client.post("/api/chat", json={"message": "First", "conversation_id": "test-session"})
    second = client.post("/api/chat", json={"message": "Second", "conversation_id": "test-session"})
    assert first.status_code == second.status_code == 200
    history = client.get("/api/conversations/test-session/history").json()["messages"]
    assert len(history) == 4
    assert history[0]["content"] == "First"
    assert history[2]["content"] == "Second"

def test_empty_message_rejected():
    assert client.post("/api/chat", json={"message": "   "}).status_code == 422

def test_delete_conversation():
    client.post("/api/chat", json={"message": "temporary", "conversation_id": "delete-me"})
    assert client.delete("/api/conversations/delete-me").json()["deleted"] is True
    assert client.get("/api/conversations/delete-me/history").json()["messages"] == []
