from unittest.mock import MagicMock, patch
from backend.app.main import get_agent_response
import pytest

@patch('backend.app.main.ChatGroq')
def test_get_agent_response(mock_chat_groq):
    # Setup mock
    mock_llm = MagicMock()
    mock_chat_groq.return_value = mock_llm
    
    # Mock AI message with content and no tool calls
    mock_ai_msg = MagicMock()
    mock_ai_msg.content = "Hello from AI"
    mock_ai_msg.tool_calls = []
    
    mock_llm.bind_tools.return_value.invoke.return_value = mock_ai_msg
    
    response = get_agent_response("Hi", "Friendly Assistant")
    assert response == "Hello from AI"
    
    # Verify model was initialized
    mock_chat_groq.assert_called()
    args, kwargs = mock_chat_groq.call_args
    assert kwargs['model'] == "llama3-70b-8192"