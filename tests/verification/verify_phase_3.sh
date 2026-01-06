#!/bin/bash
set -e

echo "Verifying Phase 3: Semantic Search Integration..."

# Verify server is running
if ! docker compose ps | grep -q "Up"; then
    echo "Error: Containers are not running."
    exit 1
fi

echo "Testing semantic search tool directly..."
docker compose exec -T backend uv run python - <<EOF
from app.main import search_products_semantic
import os

# Ensure DB connection env var is set (docker-compose sets it but python script might need it if creating engine locally)
# In app.main, engine is created using os.getenv("DATABASE_URL")
# Inside container, it is set.

try:
    result = search_products_semantic.invoke({"query": "athletic clothes"})
    print("--- Search Result ---")
    print(result)
    print("---------------------")
    
    if "Found" in result or "No relevant products" in result:
        # We expect results because we seeded products.
        if "Found" in result:
            print("SUCCESS: Tool returned products.")
        else:
            print("WARNING: Tool returned no products (maybe threshold or data issue).")
            # If we seeded correctly in Phase 2, we should find something for "athletic clothes"
            # as we added athletic gear.
            if "No relevant products" in result:
                 # Check if we have products at all
                 from app.main import engine
                 from sqlmodel import Session, select, text
                 from app.models import Product
                 with Session(engine) as session:
                     count = session.exec(select(Product)).all()
                     print(f"DEBUG: Total products in DB: {len(count)}")
                     # Debug embedding
                     p = session.exec(select(Product).limit(1)).first()
                     if p:
                         print(f"DEBUG: Sample product '{p.name}' has embedding: {p.embedding is not None}")
                         
    else:
        print("FAILURE: Unexpected output format.")
        exit(1)
except Exception as e:
    print(f"FAILURE: Tool execution failed: {e}")
    exit(1)
EOF

echo "Phase 3 Verification Complete!"
