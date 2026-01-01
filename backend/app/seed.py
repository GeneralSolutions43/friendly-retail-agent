"""Seeding script for the database."""

import os
from sqlmodel import Session, select, create_engine, SQLModel
from app.models import Product

DATABASE_URL = os.getenv("DATABASE_URL",
                         "postgresql://user:password@localhost:5432/retail_agent")
engine = create_engine(DATABASE_URL)


def seed_products():
    """Seed the database with initial products."""
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        # Check if products already exist
        statement = select(Product)
        results = session.exec(statement).first()
        if results:
            print("Products already exist, skipping seed.")
            return

        products = [
            Product(
                name="Performance Running Shoes",
                category="Footwear",
                price=120.00,
                description="High-performance running shoes for serious athletes.",
                inventory_count=50
            ),
            Product(
                name="Casual Hoodie",
                category="Apparel",
                price=45.50,
                description="Comfortable cotton hoodie for everyday wear.",
                inventory_count=100
            ),
            Product(
                name="Yoga Mat",
                category="Fitness Gear",
                price=25.00,
                description="Non-slip yoga mat for home workouts.",
                inventory_count=30
            ),
            Product(
                name="Wireless Earbuds",
                category="Electronics",
                price=89.99,
                description="True wireless earbuds with noise cancellation.",
                inventory_count=20
            ),
            Product(
                name="Water Bottle",
                category="Accessories",
                price=15.00,
                description="Stainless steel water bottle, 24oz.",
                inventory_count=200
            ),
        ]

        for product in products:
            session.add(product)

        session.commit()
        print("Database seeded with initial products.")


if __name__ == "__main__":
    seed_products()
