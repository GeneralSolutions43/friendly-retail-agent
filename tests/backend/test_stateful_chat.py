import pytest
from unittest.mock import patch, MagicMock
from langchain_core.messages import HumanMessage, AIMessage
import os
import sys

# Ensure backend is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from app.main import get_agent_response

class MockHistory:
    def __init__(self):
        self.messages = []
    
    def add_messages(self, msgs):
        self.messages.extend(msgs)

def test_multi_turn_logic():
    # Use a shared history object to simulate persistence
    shared_history = MockHistory()
    
    with patch("app.main.ChatGroq") as mock_chat_groq, \
         patch("app.main.get_chat_history") as mock_get_history:
        
        mock_get_history.return_value = shared_history
        
        # Setup LLM to return different answers
        mock_llm = MagicMock()
        mock_chat_groq.return_value = mock_llm
        mock_llm_with_tools = MagicMock()
        mock_llm.bind_tools.return_value = mock_llm_with_tools
        
        # Turn 1
        mock_llm_with_tools.invoke.return_value = MagicMock(content="Hi Alice", tool_calls=[])
        
        resp1 = get_agent_response("Hi, I'm Alice", "Friendly Assistant", session_id="session-1")
        assert resp1 == "Hi Alice"
        assert len(shared_history.messages) == 2 # Human + AI
        
        # Turn 2
        mock_llm_with_tools.invoke.return_value = MagicMock(content="Alice", tool_calls=[])
        
        resp2 = get_agent_response("Who am I?", "Friendly Assistant", session_id="session-1")
        
        # Verify the call args for the SECOND invoke
        # Note: call_args returns the LAST call.
        args, _ = mock_llm_with_tools.invoke.call_args
        messages_passed = args[0]
        
        # The messages list might be mutated (appended to) after the call.
        # We know the last item is the response Mock.
        # We verify the first 4 items are the history context.
        assert len(messages_passed) >= 4
        assert messages_passed[1].content == "Hi, I'm Alice"
        assert messages_passed[2].content == "Hi Alice"
        assert messages_passed[3].content == "Who am I?"
        assert messages_passed[1].content == "Hi, I'm Alice"
        assert messages_passed[2].content == "Hi Alice"
        assert messages_passed[3].content == "Who am I?"
