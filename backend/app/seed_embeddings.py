from sqlmodel import Session, select, create_engine
import os
from .models import Product

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://user:password@localhost:5432/retail_agent"
)
engine = create_engine(DATABASE_URL)


def seed_embeddings():
    print("Starting bulk embedding generation...")
    with Session(engine) as session:
        products = session.exec(select(Product)).all()
        print(f"Found {len(products)} products.")

        count = 0
        for product in products:
            # Force update embedding
            product.update_embedding()
            session.add(product)
            count += 1
            if count % 10 == 0:
                print(f"Processed {count} products...")

        session.commit()
        print(f"Successfully updated embeddings for {count} products.")


if __name__ == "__main__":
    seed_embeddings()
