import pytest
from unittest.mock import patch, MagicMock
from langchain_core.messages import HumanMessage, AIMessage
import os
import sys

# Ensure backend is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from app.main import get_agent_response

class MockHistory:
    def __init__(self, messages):
        self.messages = messages
        self.cleared = False
        self.added = []
    
    def clear(self):
        self.cleared = True
        self.messages = []
        
    def add_messages(self, msgs):
        self.messages.extend(msgs)
        self.added.extend(msgs)

def test_summarization_integration():
    # 12 messages (6 turns)
    long_history = [HumanMessage(content=f"Msg {i}") for i in range(12)]
    mock_history = MockHistory(long_history)
    
    with patch("app.main.ChatGroq") as mock_chat_groq, \
         patch("app.main.get_chat_history") as mock_get_history, \
         patch("app.main.summarize_messages") as mock_summarize:
        
        mock_get_history.return_value = mock_history
        mock_summarize.return_value = "This is a summary."
        
        mock_llm = MagicMock()
        mock_chat_groq.return_value = mock_llm
        mock_llm_with_tools = MagicMock()
        mock_llm.bind_tools.return_value = mock_llm_with_tools
        mock_llm_with_tools.invoke.return_value = MagicMock(content="Response", tool_calls=[])
        
        # Call agent
        get_agent_response("Current msg", "Friendly Assistant", session_id="long-session")
        
        # Verify summarizer was called
        assert mock_summarize.called
        # Verify history was cleared and updated (or at least attempted)
        assert mock_history.cleared
        # Verify summary was added back
        assert any("This is a summary" in str(m.content) for m in mock_history.messages)
