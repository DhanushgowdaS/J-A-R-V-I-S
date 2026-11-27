from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "J-A-R-V-I-S API"

def test_api_info_endpoint():
    response = client.get("/api")
    assert response.status_code == 200
    assert response.json()["name"] == "J-A-R-V-I-S"
