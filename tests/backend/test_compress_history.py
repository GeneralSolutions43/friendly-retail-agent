import pytest
from unittest.mock import patch, MagicMock
from langchain_core.messages import HumanMessage, AIMessage
import os
import sys

# Ensure backend is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from app.main import compress_history

class MockHistory:
    def __init__(self, messages):
        self.messages = messages
        self.cleared = False
    
    def clear(self):
        self.cleared = True
        self.messages = []
        
    def add_messages(self, msgs):
        self.messages.extend(msgs)

def test_compress_history_logic():
    # 14 messages
    messages = [HumanMessage(content=f"Msg {i}") for i in range(14)]
    history = MockHistory(messages)
    
    with patch("app.main.summarize_messages") as mock_summarize:
        mock_summarize.return_value = "Summary"
        
        compress_history(history, threshold=10)
        
        assert history.cleared
        # Result should be: [Summary] + messages[-4:]
        assert len(history.messages) == 5
        assert "[System: Summary" in history.messages[0].content
        assert history.messages[1].content == "Msg 10"
        assert history.messages[-1].content == "Msg 13"

def test_compress_history_no_trigger():
    # 8 messages (below threshold 10)
    messages = [HumanMessage(content=f"Msg {i}") for i in range(8)]
    history = MockHistory(messages)
    
    with patch("app.main.summarize_messages") as mock_summarize:
        compress_history(history, threshold=10)
        
        assert not history.cleared
        assert len(history.messages) == 8
        assert not mock_summarize.called
