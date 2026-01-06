from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, select
from sqlmodel.pool import StaticPool
from backend.app.main import app, get_session
from backend.app.models import Product
import pytest

# Create an in-memory SQLite database for testing
engine = create_engine(
    "sqlite:///:memory:", 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)

def create_test_database():
    # Ensure tables are created on the test engine
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        # Check if data exists
        if session.exec(select(Product)).first():
            return
        product1 = Product(name="Test Product 1", category="Cat 1", price=10.0, description="Desc 1", inventory_count=5)
        product2 = Product(name="Test Product 2", category="Cat 2", price=20.0, description="Desc 2", inventory_count=10)
        session.add(product1)
        session.add(product2)
        session.commit()

# Dependency override
def get_session_override():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = get_session_override

client = TestClient(app)

def test_get_all_products():
    create_test_database()
    response = client.get("/products")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    assert any(p["name"] == "Test Product 1" for p in data)
    assert any(p["name"] == "Test Product 2" for p in data)

def test_products_serialization_numpy_error():
    """
    Test that reproduces the PydanticSerializationError when a product has a numpy array as embedding.
    """
    import numpy as np
    from unittest.mock import patch
    
    # Mock data with a numpy array for embedding
    mock_product = Product(
        id=999,
        name="Numpy Product",
        category="Test",
        price=10.0,
        description="Test Description",
        inventory_count=1
    )
    # Manually set embedding to a numpy array to simulate what might come from the DB
    mock_product.embedding = np.array([0.1, 0.2, 0.3], dtype=np.float32)
    
    with patch("backend.app.main.Session.exec") as mock_exec:
        mock_exec.return_value.all.return_value = [mock_product]
        
        # This call should trigger the serialization error if 'embedding' is included
        # and not handled by a custom serializer.
        response = client.get("/products")
        assert response.status_code == 200
        data = response.json()
        assert data[0]["name"] == "Numpy Product"
        # Verify 'embedding' is NOT in the response
        assert "embedding" not in data[0]

def test_search_products_excludes_embedding():
    """
    Test that the search endpoint also excludes the embedding field.
    """
    create_test_database()
    response = client.get("/products/search?query=Test")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        for p in data:
            assert "embedding" not in p