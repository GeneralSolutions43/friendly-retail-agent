import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from langchain_core.messages import HumanMessage, AIMessage
import os
import sys
import json

# Ensure backend is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from app.main import get_streaming_agent_response

@pytest.mark.anyio
async def test_get_streaming_agent_response_accepts_session_id():
    with patch("app.main.ChatGroq") as mock_chat_groq, \
         patch("app.main.get_chat_history") as mock_get_history:
        
        mock_llm = MagicMock()
        mock_chat_groq.return_value = mock_llm
        mock_llm_with_tools = MagicMock()
        mock_llm.bind_tools.return_value = mock_llm_with_tools
        
        # Mock astream
        mock_ai_msg = MagicMock(content="Hello", tool_calls=[])
        async def mock_astream(*args, **kwargs):
            yield mock_ai_msg
            
        mock_llm_with_tools.astream = mock_astream
        
        mock_history = MagicMock()
        mock_history.messages = []
        mock_get_history.return_value = mock_history
        
        try:
            generator = get_streaming_agent_response("hi", "Helpful Professional", session_id="test-session")
            async for chunk in generator:
                assert "Hello" in chunk
        except TypeError as e:
            if "session_id" in str(e):
                pytest.fail(f"get_streaming_agent_response does not accept session_id: {e}")
            raise e

@pytest.mark.anyio
async def test_get_streaming_agent_response_saves_to_history():
    with patch("app.main.ChatGroq") as mock_chat_groq, \
         patch("app.main.get_chat_history") as mock_get_history:
        
        mock_llm = MagicMock()
        mock_chat_groq.return_value = mock_llm
        mock_llm_with_tools = MagicMock()
        mock_llm.bind_tools.return_value = mock_llm_with_tools
        
        mock_ai_msg = MagicMock(content="Streaming response", tool_calls=[])
        async def mock_astream(*args, **kwargs):
            yield mock_ai_msg
    
        mock_llm_with_tools.astream = mock_astream
        
        mock_history = MagicMock()
        mock_history.messages = []
        mock_get_history.return_value = mock_history
        
        generator = get_streaming_agent_response("New message", "Helpful Professional", session_id="test-session")
        async for _ in generator:
            pass
            
        # Verify history was fetched
        mock_get_history.assert_called_with("test-session")
        
        # Verify messages added to history
        assert mock_history.add_messages.called
        args, _ = mock_history.add_messages.call_args
        messages = args[0]
        assert isinstance(messages[0], HumanMessage)
        assert messages[0].content == "New message"
        assert isinstance(messages[1], AIMessage)
        assert messages[1].content == "Streaming response"
