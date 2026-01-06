from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.app.main import app

client = TestClient(app)

def test_chat_endpoint_mocked():
    # Test Helpful Professional tone
    payload = {
        "message": "Hello",
        "tone": "Helpful Professional"
    }
    
    with patch('backend.app.main.get_agent_response') as mock_agent:
        mock_agent.return_value = "AI response"
        response = client.post("/chat", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["response"] == "AI response"
        assert data["tone"] == "Helpful Professional"
        mock_agent.assert_called_with("Hello", "Helpful Professional")

def test_chat_invalid_tone():
    payload = {
        "message": "Hello",
        "tone": "Rude"
    }
    response = client.post("/chat", json=payload)
    assert response.status_code == 422 # Validation error