from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.app.main import app

client = TestClient(app)

def test_cors_headers():
    # Simulate a request from the frontend origin
    origin = "http://localhost:3002"
    headers = {
        "Origin": origin,
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "content-type",
    }
    
    # Preflight request
    response = client.options("/chat", headers=headers)
    
    # The status code should be 200 for a successful preflight
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == origin
    assert "POST" in response.headers["access-control-allow-methods"]
    assert "content-type" in response.headers["access-control-allow-headers"]

    # Actual request - mock agent response to avoid requiring API key
    with patch('backend.app.main.get_agent_response') as mock_agent:
        mock_agent.return_value = "AI response"
        response = client.post(
            "/chat", 
            json={"message": "test", "tone": "Helpful Professional"},
            headers={"Origin": origin}
        )
        assert response.status_code == 200
        assert response.headers["access-control-allow-origin"] == origin