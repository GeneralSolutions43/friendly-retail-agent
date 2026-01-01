import pytest
from sqlmodel import SQLModel, create_engine, Session, select
from backend.app.models import Product

# Use an in-memory SQLite database for testing the schema
engine = create_engine("sqlite:///:memory:")

def test_create_product():
    SQLModel.metadata.create_all(engine)
    product = Product(
        name="Running Shoes",
        category="Footwear",
        price=99.99,
        description="Great for running",
        inventory_count=10
    )
    with Session(engine) as session:
        session.add(product)
        session.commit()
        session.refresh(product)
        
        assert product.id is not None
        assert product.name == "Running Shoes"
        
        statement = select(Product).where(Product.name == "Running Shoes")
        result = session.exec(statement).first()
        assert result is not None
        assert result.category == "Footwear"
