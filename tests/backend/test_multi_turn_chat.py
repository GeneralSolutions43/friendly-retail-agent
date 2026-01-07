import pytest
from unittest.mock import patch, MagicMock
from langchain_core.messages import HumanMessage, SystemMessage
import os
import sys

# Ensure backend is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from app.main import get_agent_response

def test_get_agent_response_accepts_session_id():
    with patch("app.main.ChatGroq") as mock_chat_groq, \
         patch("app.main.get_chat_history") as mock_get_history:
        
        mock_llm = MagicMock()
        mock_chat_groq.return_value = mock_llm
        mock_llm_with_tools = MagicMock()
        mock_llm.bind_tools.return_value = mock_llm_with_tools
        mock_llm_with_tools.invoke.return_value = MagicMock(content="Hello", tool_calls=[])
        
        mock_history = MagicMock()
        mock_history.messages = []
        mock_get_history.return_value = mock_history
        
        # This will fail if get_agent_response doesn't accept session_id
        try:
            response = get_agent_response("hi", "Helpful Professional", session_id="test-session")
            assert response == "Hello"
        except TypeError as e:
            if "session_id" in str(e):
                pytest.fail(f"get_agent_response does not accept session_id: {e}")
            raise e

def test_get_agent_response_appends_to_history():
    with patch("app.main.ChatGroq") as mock_chat_groq, \
         patch("app.main.get_chat_history") as mock_get_history:
        
        mock_llm = MagicMock()
        mock_chat_groq.return_value = mock_llm
        mock_llm_with_tools = MagicMock()
        mock_llm.bind_tools.return_value = mock_llm_with_tools
        mock_llm_with_tools.invoke.return_value = MagicMock(content="Final Response", tool_calls=[])
        
        mock_history = MagicMock()
        mock_history.messages = [HumanMessage(content="Old message")]
        mock_get_history.return_value = mock_history
        
        get_agent_response("New message", "Helpful Professional", session_id="test-session")
        
        # Verify history was fetched
        mock_get_history.assert_called_with("test-session")
        
        # Verify messages added to history (Human message and AI response)
        assert mock_history.add_messages.called
