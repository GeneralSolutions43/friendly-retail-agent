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
            # For this track, we want to allow adding NEW products even if some exist
            # but we will check for specific names to avoid duplicates
            existing_names = session.exec(select(Product.name)).all()
        else:
            existing_names = []

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
            # New Athletic Apparel
            Product(
                name="Pro-Performance Leggings",
                category="Apparel",
                price=65.00,
                description="High-compression leggings for intense workouts.",
                inventory_count=75
            ),
            Product(
                name="Breathable Mesh Training Shirt",
                category="Apparel",
                price=35.00,
                description="Moisture-wicking mesh shirt for superior ventilation.",
                inventory_count=120
            ),
            Product(
                name="Elite Lightweight Running Shorts",
                category="Apparel",
                price=40.00,
                description="Ultra-light shorts with built-in liner for runners.",
                inventory_count=90
            ),
            Product(
                name="Thermal Windbreaker Jacket",
                category="Apparel",
                price=85.00,
                description="Weather-resistant jacket for cold-weather training.",
                inventory_count=45
            ),
            Product(
                name="Seamless Sports Bra",
                category="Apparel",
                price=30.00,
                description="Medium-support seamless bra for all-day comfort.",
                inventory_count=150
            ),
            Product(
                name="Compression Tech Sleeves",
                category="Apparel",
                price=25.00,
                description="Graduated compression sleeves for muscle recovery.",
                inventory_count=60
            ),
            Product(
                name="Quick-Dry Athletic Tank",
                category="Apparel",
                price=28.00,
                description="Lightweight tank top designed for high mobility.",
                inventory_count=110
            ),
            Product(
                name="Water-Repellent Trail Pants",
                category="Apparel",
                price=75.00,
                description="Durable trail pants with DWR finish for outdoor use.",
                inventory_count=40
            ),
            Product(
                name="Merino Wool Base Layer",
                category="Apparel",
                price=95.00,
                description="Natural moisture-wicking base layer for extreme cold.",
                inventory_count=35
            ),
            Product(
                name="Impact-Absorption Socks",
                category="Apparel",
                price=18.00,
                description="Cushioned athletic socks for high-impact activities.",
                inventory_count=300
            ),
            Product(
                name="Fleece-Lined Running Tights",
                category="Apparel",
                price=70.00,
                description="Insulated tights for winter running performance.",
                inventory_count=55
            ),
            Product(
                name="Adjustable Reflective Vest",
                category="Apparel",
                price=32.00,
                description="High-visibility vest for safe nighttime training.",
                inventory_count=80
            ),
        ]

        added_count = 0
        for product in products:
            if product.name not in existing_names:
                session.add(product)
                added_count += 1

        session.commit()
        if added_count > 0:
            print(f"Database seeded with {added_count} new products.")
        else:
            print("No new products to seed.")


if __name__ == "__main__":
    seed_products()
