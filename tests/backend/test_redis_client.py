import pytest
from unittest.mock import patch, MagicMock
import os
import sys

# Ensure backend/app can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

# We expect this import to fail initially
try:
    from app.redis_client import get_redis_client
except ImportError:
    get_redis_client = None

def test_get_redis_client_importable():
    assert get_redis_client is not None, "Could not import get_redis_client from app.redis_client"

def test_get_redis_client_connection():
    if get_redis_client is None:
        pytest.fail("Module app.redis_client not found")
        
    with patch("redis.from_url") as mock_from_url:
        mock_client = MagicMock()
        mock_from_url.return_value = mock_client
        
        # Set env var
        os.environ["REDIS_URL"] = "redis://test-redis:6379/1"
        
        client = get_redis_client()
        
        mock_from_url.assert_called_with("redis://test-redis:6379/1", decode_responses=True)
        assert client == mock_client
