#!/bin/bash
set -e

echo "Verifying Phase 1: Infrastructure & Environment Setup..."

# Verify server is running
if ! docker compose ps | grep -q "Up"; then
    echo "Error: Containers are not running."
    exit 1
fi

# Verify DB extension and schema
echo "Checking DB schema..."
docker compose exec -T backend uv run python - <<EOF
from sqlmodel import create_engine, inspect, text, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# Check Extension
with Session(engine) as session:
    ext = session.exec(text("SELECT * FROM pg_extension WHERE extname = 'vector'")).first()
    if not ext:
        print("FAILURE: pgvector extension NOT enabled.")
        exit(1)
    print("SUCCESS: pgvector extension enabled.")

# Check Column
inspector = inspect(engine)
cols = [c["name"] for c in inspector.get_columns("product")]
if "embedding" not in cols:
    print("FAILURE: embedding column NOT found in product table.")
    exit(1)
print("SUCCESS: embedding column found in product table.")
EOF

echo "Phase 1 Verification Complete!"