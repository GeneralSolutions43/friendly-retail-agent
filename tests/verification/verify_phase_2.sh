#!/bin/bash
set -e

echo "Verifying Phase 2: Embedding Service & Real-time Sync..."

# Verify server is running
if ! docker compose ps | grep -q "Up"; then
    echo "Error: Containers are not running."
    exit 1
fi

echo "Seeding products..."
docker compose exec -T backend uv run python -m app.seed

echo "Running bulk embedding seed..."
docker compose exec -T backend uv run python -m app.seed_embeddings

echo "Verifying data in DB..."
docker compose exec -T backend uv run python - <<EOF
from sqlmodel import create_engine, select, Session
from app.models import Product
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

with Session(engine) as session:
    # Check if ANY product has an embedding
    statement = select(Product).where(Product.embedding != None)
    product = session.exec(statement).first()
    
    if product:
        print(f"SUCCESS: Found product '{product.name}' with embedding length {len(product.embedding)}")
    else:
        print("FAILURE: No products found with embeddings.")
        exit(1)
EOF

echo "Phase 2 Verification Complete!"
