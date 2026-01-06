# Plan: RAG Implementation (Product Knowledge)

## Phase 1: Infrastructure & Environment Setup
- [x] Task: Update Backend dependencies. Add `sentence-transformers` and `torch` (CPU) to `backend/requirements.txt`. [commit: df8de79]
- [x] Task: Configure Database for `pgvector`. Update `docker-compose.yml` (if necessary) and verify `pgvector` extension can be enabled. [commit: b132ca0]
- [ ] Task: Create Vector Index. Implement a migration or script to enable the `vector` extension and add an `embedding` column to the `Product` table.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Infrastructure & Environment Setup' (Protocol in workflow.md)

## Phase 2: Embedding Service & Real-time Sync
- [ ] Task: Implement Embedding Utility. Create `backend/app/embeddings.py` using `SentenceTransformers`.
- [ ] Task: Test Embedding Utility. Write unit tests to verify embedding generation (Red/Green/Refactor).
- [ ] Task: Implement Automatic Sync. Update the `Product` creation/update logic to generate and store embeddings in real-time.
- [ ] Task: Test Automatic Sync. Write unit tests to verify that saving a product updates its embedding (Red/Green/Refactor).
- [ ] Task: Bulk Seeding Script. Create a script to generate embeddings for existing products in the database.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Embedding Service & Real-time Sync' (Protocol in workflow.md)

## Phase 3: Semantic Search Integration
- [ ] Task: Implement Semantic Search Tool. Create `search_products_semantic` tool for the LangChain agent.
- [ ] Task: Test Semantic Search Tool. Write unit tests to verify vector similarity results (Red/Green/Refactor).
- [ ] Task: Enhance Agent Logic. Integrate the semantic search tool into the `get_agent_response` workflow.
- [ ] Task: Test End-to-End Search. Verify the agent can answer semantic queries (e.g., "Recommend winter gear") in the chat (Red/Green/Refactor).
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Semantic Search Integration' (Protocol in workflow.md)

## Phase 4: Refinement & Polish
- [ ] Task: Optimize Vector Search. Add an HNSW index to the embedding column for better performance.
- [ ] Task: Final UI/UX Check. Ensure the agent's responses using RAG data are natural and well-formatted.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Refinement & Polish' (Protocol in workflow.md)
