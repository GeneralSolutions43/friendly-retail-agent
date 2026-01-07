for i in {1..11}; do
    curl -X POST http://localhost:8002/chat \
        -H "Content-Type: application/json" \
        -d "{\"message\": \"Counting $i\", \"tone\": \"Friendly Assistant\", \"session_id\": \"summarize-test\"}"
    done
