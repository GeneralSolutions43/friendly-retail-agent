# Plan: RAG Implementation (Product Knowledge)

## Phase 1: Infrastructure & Environment Setup
- [x] Task: Update Backend dependencies. Add `sentence-transformers` and `torch` (CPU) to `backend/requirements.txt`. [commit: df8de79]
- [x] Task: Configure Database for `pgvector`. Update `docker-compose.yml` (if necessary) and verify `pgvector` extension can be enabled. [commit: b132ca0]
- [x] Task: Create Vector Index. Implement a migration or script to enable the `vector` extension and add an `embedding` column to the `Product` table. [commit: 13d6317]
- [x] Task: Conductor - User Manual Verification 'Phase 1: Infrastructure & Environment Setup' (Protocol in workflow.md) [checkpoint: cee3cdd]

## Phase 2: Embedding Service & Real-time Sync
- [x] Task: Implement Embedding Utility. Create `backend/app/embeddings.py` using `SentenceTransformers`. [commit: 59bf0d6]
- [x] Task: Test Embedding Utility. Write unit tests to verify embedding generation (Red/Green/Refactor). [commit: 59bf0d6]
- [x] Task: Implement Automatic Sync. Update the `Product` creation/update logic to generate and store embeddings in real-time. [commit: a1839c8]
- [x] Task: Test Automatic Sync. Write unit tests to verify that saving a product updates its embedding (Red/Green/Refactor). [commit: a1839c8]
- [x] Task: Bulk Seeding Script. Create a script to generate embeddings for existing products in the database. [commit: c79a283]
- [x] Task: Conductor - User Manual Verification 'Phase 2: Embedding Service & Real-time Sync' (Protocol in workflow.md) [checkpoint: ac9dc82]

## Phase 3: Semantic Search Integration
- [x] Task: Implement Semantic Search Tool. Create `search_products_semantic` tool for the LangChain agent. [commit: aa728c0]
- [x] Task: Test Semantic Search Tool. Write unit tests to verify vector similarity results (Red/Green/Refactor). [commit: aa728c0]
- [x] Task: Enhance Agent Logic. Integrate the semantic search tool into the `get_agent_response` workflow. [commit: 30dfc64]
- [x] Task: Test End-to-End Search. Verify the agent can answer semantic queries (e.g., "Recommend winter gear") in the chat (Red/Green/Refactor). [commit: 3a88430]
- [x] Task: Conductor - User Manual Verification 'Phase 3: Semantic Search Integration' (Protocol in workflow.md) [checkpoint: 25a5339]

## Phase 4: Refinement & Polish
- [x] Task: Optimize Vector Search. Add an HNSW index to the embedding column for better performance. [commit: 0e0ab65]
- [x] Task: Final UI/UX Check. Ensure the agent's responses using RAG data are natural and well-formatted. [commit: 1ecc619]
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Refinement & Polish' (Protocol in workflow.md)
