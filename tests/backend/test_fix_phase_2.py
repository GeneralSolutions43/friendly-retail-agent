from unittest.mock import MagicMock, patch
import pytest
from backend.app.main import get_agent_response, app
from fastapi.testclient import TestClient

client = TestClient(app)

@patch('backend.app.main.ChatGroq')
def test_reproduce_music_exercise_blank(mock_chat_groq):
    # Setup mock LLM
    mock_llm = MagicMock()
    mock_chat_groq.return_value = mock_llm
    
    # Mock AI message with EMPTY content to simulate the reported bug
    mock_ai_msg = MagicMock()
    mock_ai_msg.content = ""
    mock_ai_msg.tool_calls = []
    
    mock_bound_llm = mock_llm.bind_tools.return_value
    mock_bound_llm.invoke.return_value = mock_ai_msg
    
    payload = {
        "message": "I like to listen to music when I exercise",
        "tone": "Friendly Assistant"
    }
    
    response = client.post("/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    # It should now return the fallback message instead of being blank
    assert data["response"] == "I'm sorry, I encountered an issue processing that. Could you try rephrasing?"

@patch('backend.app.main.ChatGroq')
def test_music_exercise_acknowledgement(mock_chat_groq):
    # Setup mock LLM
    mock_llm = MagicMock()
    mock_chat_groq.return_value = mock_llm
    
    # Mock AI message with meaningful content
    mock_ai_msg = MagicMock()
    mock_ai_msg.content = "That's great! Music is a wonderful motivator for exercise. Are you looking for any specific gear like headphones for your workouts?"
    mock_ai_msg.tool_calls = []
    
    mock_bound_llm = mock_llm.bind_tools.return_value
    mock_bound_llm.invoke.return_value = mock_ai_msg
    
    response = get_agent_response("I like to listen to music when I exercise", "Friendly Assistant")
    assert "Music is a wonderful motivator" in response
