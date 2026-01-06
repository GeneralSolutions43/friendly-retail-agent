from unittest.mock import MagicMock, patch
import pytest
from backend.app.main import get_agent_response, app
from fastapi.testclient import TestClient

client = TestClient(app)

@patch('backend.app.main.ChatGroq')
def test_reproduce_sore_muscles_blank(mock_chat_groq):
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
        "message": "Do you have anything that will help when my muscles are sore?",
        "tone": "Expert Consultant"
    }
    
    response = client.post("/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    # It should now return the fallback message instead of being blank
    assert data["response"] == "I'm sorry, I encountered an issue processing that. Could you try rephrasing?"

@patch('backend.app.main.ChatGroq')
def test_sore_muscles_tool_triggering(mock_chat_groq):
    # Setup mock LLM
    mock_llm = MagicMock()
    mock_chat_groq.return_value = mock_llm
    
    # Mock first call with tool call
    mock_ai_msg_with_tool = MagicMock()
    mock_ai_msg_with_tool.content = ""
    mock_ai_msg_with_tool.tool_calls = [{
        "name": "search_products_semantic",
        "args": {"query": "muscle recovery gear sore muscles"},
        "id": "call_123"
    }]
    
    # Mock second call (final response)
    mock_final_msg = MagicMock()
    mock_final_msg.content = "I found some great options for muscle recovery! We have massage balls and foam rollers that are perfect for sore muscles."
    
    mock_bound_llm = mock_llm.bind_tools.return_value
    # Use side_effect to return different values on sequential calls
    mock_bound_llm.invoke.side_effect = [mock_ai_msg_with_tool, mock_final_msg]
    
    # We also need to mock search_products_semantic to return something
    with patch('backend.app.main.search_products_semantic') as mock_tool:
        mock_tool.return_value = "Found massage ball and foam roller."
        response = get_agent_response("Do you have anything that will help when my muscles are sore?", "Expert Consultant")
        
    assert "massage balls and foam rollers" in response
    mock_tool.invoke.assert_called_once()
