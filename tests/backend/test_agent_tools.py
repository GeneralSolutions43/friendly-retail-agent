from sqlmodel import Session, SQLModel, create_engine, select
from sqlmodel.pool import StaticPool
from backend.app.main import search_products_tool
from backend.app.models import Product
import pytest

# Create an in-memory SQLite database for testing
engine = create_engine(
    "sqlite:///:memory:", 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)

# We need to monkeypatch the engine in search_products_tool to use our test engine
import backend.app.main

def setup_module(module):
    backend.app.main.engine = engine
    Product.metadata.create_all(engine)
    with Session(engine) as session:
        product1 = Product(name="Tool Test Shoe", category="Footwear", price=100.0, description="Comfortable", inventory_count=10)
        session.add(product1)
        session.commit()

def test_search_products_tool():
    result = search_products_tool.invoke({"query": "Shoe"})
    assert "Tool Test Shoe" in result
    assert "Footwear" in result
    
    result = search_products_tool.invoke({"query": "Nothing"})
    assert "No products found" in result
