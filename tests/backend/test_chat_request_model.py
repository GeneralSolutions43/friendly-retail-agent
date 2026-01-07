from app.main import ChatRequest
import pytest
from pydantic import ValidationError

def test_chat_request_with_session_id():
    request = ChatRequest(message="hello", tone="Friendly Assistant", session_id="test-session")
    assert request.session_id == "test-session"

def test_chat_request_optional_session_id():
    request = ChatRequest(message="hello", tone="Friendly Assistant")
    # This will fail if session_id is not defined in the model
    try:
        assert hasattr(request, "session_id")
    except AttributeError:
        pytest.fail("ChatRequest does not have session_id attribute")
