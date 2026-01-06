from unittest.mock import MagicMock, patch
import pytest
from backend.app.main import get_agent_response, app
from fastapi.testclient import TestClient

client = TestClient(app)

@patch('backend.app.main.ChatGroq')
def test_get_agent_response_empty_fails(mock_chat_groq):
    # Setup mock LLM
    mock_llm = MagicMock()
    mock_chat_groq.return_value = mock_llm
    
    # Mock AI message with EMPTY content
    mock_ai_msg = MagicMock()
    mock_ai_msg.content = ""
    mock_ai_msg.tool_calls = []
    
    mock_bound_llm = mock_llm.bind_tools.return_value
    mock_bound_llm.invoke.return_value = mock_ai_msg
    
    with pytest.raises(ValueError, match="AI generated an empty response."):
        get_agent_response("Hi", "Friendly Assistant")

@patch('backend.app.main.ChatGroq')
def test_chat_endpoint_fallback(mock_chat_groq):
    # Setup mock LLM
    mock_llm = MagicMock()
    mock_chat_groq.return_value = mock_llm
    
    # Mock AI message with EMPTY content
    mock_ai_msg = MagicMock()
    mock_ai_msg.content = ""
    mock_ai_msg.tool_calls = []
    
    mock_bound_llm = mock_llm.bind_tools.return_value
    mock_bound_llm.invoke.return_value = mock_ai_msg
    
    payload = {
        "message": "Hi",
        "tone": "Friendly Assistant"
    }
    
    response = client.post("/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["response"] == "I'm sorry, I encountered an issue processing that. Could you try rephrasing?"

@patch('backend.app.main.ChatGroq')
def test_get_agent_response_success(mock_chat_groq):
    # Setup mock LLM
    mock_llm = MagicMock()
    mock_chat_groq.return_value = mock_llm
    
    # Mock AI message with content
    mock_ai_msg = MagicMock()
    mock_ai_msg.content = "Hello there!"
    mock_ai_msg.tool_calls = []
    
    mock_bound_llm = mock_llm.bind_tools.return_value
    mock_bound_llm.invoke.return_value = mock_ai_msg
    
    response = get_agent_response("Hi", "Friendly Assistant")
    assert response == "Hello there!"
