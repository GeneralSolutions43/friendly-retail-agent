#!/bin/bash
set -e

echo "Verifying Phase 4: Refinement & Polish..."

# Verify server is running
if ! docker compose ps | grep -q "Up"; then
    echo "Error: Containers are not running."
    exit 1
fi

echo "Checking for HNSW index..."
docker compose exec -T backend uv run python - <<EOF
from sqlmodel import create_engine, text, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

with Session(engine) as session:
    res = session.exec(text("SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'product' AND indexname = 'product_embedding_idx'")).first()
    if res:
        print(f"SUCCESS: Index found: {res.indexname}")
        if "hnsw" in res.indexdef:
             print("SUCCESS: Index uses HNSW.")
        else:
             print(f"FAILURE: Index def does not mention hnsw: {res.indexdef}")
             exit(1)
    else:
        print("FAILURE: Index not found.")
        exit(1)
EOF

echo "Phase 4 Verification Complete!"
