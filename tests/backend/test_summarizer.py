import pytest
from unittest.mock import patch, MagicMock
from langchain_core.messages import HumanMessage, AIMessage
import os
import sys

# Ensure backend is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

try:
    from app.summarizer import summarize_messages
except ImportError:
    summarize_messages = None

def test_summarize_messages_importable():
    assert summarize_messages is not None

def test_summarize_messages_logic():
    if summarize_messages is None:
        pytest.fail("summarize_messages not found")
        
    messages = [
        HumanMessage(content="I am looking for a blue shirt"),
        AIMessage(content="I found some blue shirts for you.")
    ]
    
    with patch("app.summarizer.ChatGroq") as mock_chat, \
         patch("app.summarizer.GROQ_API_KEY", "fake-key"):
        mock_llm = MagicMock()
        mock_chat.return_value = mock_llm
        mock_llm.invoke.return_value = MagicMock(content="The user is interested in blue shirts.")
        
        summary = summarize_messages(messages)
        
        assert "blue" in summary.lower()
        # Verify it was called with some prompt containing the messages
        args, _ = mock_llm.invoke.call_args
        prompt_msgs = args[0]
        assert any("I am looking for a blue shirt" in str(m.content) for m in prompt_msgs)
