from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from backend.app.main import app, get_session
from backend.app.models import Product
import pytest

# Create an in-memory SQLite database for testing
# Use StaticPool to share the same in-memory database across sessions
engine = create_engine(
    "sqlite:///:memory:", 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)

def create_test_database():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        # Check if data exists to avoid duplicate seed if function called multiple times
        if session.exec(select(Product)).first():
            return
            
        product1 = Product(name="Test Shoe", category="Footwear", price=100.0, description="Test description", inventory_count=10)
        product2 = Product(name="Test Shirt", category="Apparel", price=50.0, description="Test description", inventory_count=10)
        session.add(product1)
        session.add(product2)
        session.commit()

from sqlmodel import select

# Dependency override
def get_session_override():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = get_session_override

client = TestClient(app)

def test_search_products():
    create_test_database()
    response = client.get("/products/search?query=Shoe")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] == "Test Shoe"
    
    response = client.get("/products/search?query=NonExistent")
    assert response.status_code == 200
    assert len(response.json()) == 0