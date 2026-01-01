from fastapi.testclient import TestClient
import pytest

# We will create the main app in backend/app/main.py
try:
    from backend.app.main import app
except ImportError:
    app = None

client = TestClient(app) if app else None

def test_health_check():
    if client is None:
        pytest.fail("FastAPI app not initialized")
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
