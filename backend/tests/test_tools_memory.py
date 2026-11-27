from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_tools_registry_and_calculator():
    tools=client.get("/api/tools").json()["tools"]
    names={t["name"] for t in tools}
    assert {"calculator","current_time"} <= names
    assert client.post("/api/tools/calculator/execute",json={"expression":"(2+3)*4"}).json()["result"]["result"] == 20

def test_calculator_rejects_code():
    response=client.post("/api/tools/calculator/execute",json={"expression":"__import__('os').system('echo bad')"})
    assert response.status_code==400

def test_unknown_tool_not_exposed():
    assert client.post("/api/tools/shell/execute",json={}).status_code==404

def test_memory_create_list_delete():
    created=client.post("/api/memory",json={"content":"test memory","category":"test"})
    assert created.status_code==200
    memory_id=created.json()["id"]
    memories=client.get("/api/memory?category=test").json()["memories"]
    assert any(m["id"]==memory_id and m["content"]=="test memory" for m in memories)
    assert client.delete(f"/api/memory/{memory_id}").json()["deleted"] is True
