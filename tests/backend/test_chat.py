from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_chat_endpoint():
    # Test Helpful Professional tone
    payload = {
        "message": "Hello",
        "tone": "Helpful Professional"
    }
    response = client.post("/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert data["tone"] == "Helpful Professional"

    # Test Friendly Assistant tone
    payload = {
        "message": "Hi there!",
        "tone": "Friendly Assistant"
    }
    response = client.post("/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["tone"] == "Friendly Assistant"

def test_chat_invalid_tone():
    payload = {
        "message": "Hello",
        "tone": "Rude"
    }
    response = client.post("/chat", json=payload)
    assert response.status_code == 422 # Validation error
