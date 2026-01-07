import pytest
from unittest.mock import patch, MagicMock
import os
import sys

# Ensure backend is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

try:
    from app.main import get_chat_history
except ImportError:
    get_chat_history = None

def test_get_chat_history_exists():
    assert get_chat_history is not None

def test_get_chat_history_invocation():
    if get_chat_history is None:
        pytest.fail("get_chat_history not found in app.main")
        
    with patch("app.main.RedisChatMessageHistory") as mock_redis_history:
        mock_instance = MagicMock()
        mock_redis_history.return_value = mock_instance
        
        history = get_chat_history("session-123")
        
        # Verify it uses the session_id and some redis_url
        args, kwargs = mock_redis_history.call_args
        assert kwargs.get("session_id") == "session-123" or args[0] == "session-123"
        assert history == mock_instance
