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