from sqlmodel import Session, SQLModel, create_engine, select
from sqlmodel.pool import StaticPool
from backend.app.seed import seed_products
from backend.app.models import Product
import backend.app.seed
import pytest

# Create an in-memory SQLite database for testing
test_engine = create_engine(
    "sqlite:///:memory:", 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)

def test_seed_products_idempotency():
    # Monkeypatch the engine used in seed_products
    backend.app.seed.engine = test_engine
    
    # Run seeding first time
    seed_products()
    
    with Session(test_engine) as session:
        count1 = len(session.exec(select(Product)).all())
        assert count1 > 0
        
    # Run seeding second time
    seed_products()
    
    with Session(test_engine) as session:
        count2 = len(session.exec(select(Product)).all())
        assert count1 == count2, "Seeding added duplicate products on second run"

def test_seed_products_adds_new():
    # Setup with some data already there
    Product.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        p = Product(name="Old Product", category="Cat", price=10, description="D", inventory_count=1)
        session.add(p)
        session.commit()
        
    backend.app.seed.engine = test_engine
    seed_products()
    
    with Session(test_engine) as session:
        all_products = session.exec(select(Product)).all()
        assert any(p.name == "Pro-Performance Leggings" for p in all_products)
        assert any(p.name == "Old Product" for p in all_products)
