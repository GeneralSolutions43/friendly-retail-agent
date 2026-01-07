from fastapi.testclient import TestClient
from unittest.mock import patch
import json
from backend.app.main import app

client = TestClient(app)

def test_chat_stream_endpoint_mocked():
    """Test the streaming chat endpoint with a mocked response."""
    payload = {
        "message": "Hello",
        "tone": "Helpful Professional"
    }
    
    # Mocking a generator for streaming tokens
    def mock_stream_generator(message, tone):
        tokens = ["Hello", "!", " How", " can", " I", " help?"]
        for token in tokens:
            yield f"data: {json.dumps({'response': token, 'tone': tone})}\n\n"

    with patch('backend.app.main.get_streaming_agent_response') as mock_streaming_agent:
        mock_streaming_agent.return_value = mock_stream_generator("Hello", "Helpful Professional")
        
        response = client.post("/chat/stream", json=payload)
        
        # If it's a StreamingResponse, TestClient handles it but we might need to iterate
        assert response.status_code == 200
        
        # SSE format: data: {...}\n\n
        content = response.text
        assert "data: {\"response\": \"Hello\", \"tone\": \"Helpful Professional\"}" in content
        assert "data: {\"response\": \"!\", \"tone\": \"Helpful Professional\"}" in content
        assert "data: {\"response\": \" help?\", \"tone\": \"Helpful Professional\"}" in content

def test_chat_stream_invalid_tone():
    """Test the streaming chat endpoint with an invalid tone."""
    payload = {
        "message": "Hello",
        "tone": "Rude"
    }
    response = client.post("/chat/stream", json=payload)
    assert response.status_code == 422 # Validation error

