import pytest
from sqlmodel import Session, SQLModel, create_engine
from app.models import Product
from pgvector.sqlalchemy import Vector

# Mock database url - we might need a real DB connection for pgvector type to work fully?
# Or just test the model definition.
# If I use sqlite, pgvector won't work. I need postgres.
# I'll rely on the model definition test first.

def test_product_has_embedding_field():
    # This should fail if field doesn't exist
    product = Product(
        name="Test Item", 
        category="Test", 
        price=10.0, 
        description="Desc", 
        embedding=[0.1] * 384
    )
    assert hasattr(product, "embedding")
    assert len(product.embedding) == 384
