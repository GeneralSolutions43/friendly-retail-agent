# Spec: RAG Implementation (Product Knowledge)

## Overview
Implement Retrieval-Augmented Generation (RAG) to enable the Friendly Retail Agent to provide accurate and context-aware information about the product catalog. This involves using semantic vector search to find relevant products based on user intent, moving beyond simple keyword matching.

## Functional Requirements
- **Semantic Search Capability:** The AI agent must be able to search for products based on the meaning of the user's query (e.g., finding "warm winter gear" when a user asks for "something for the snow").
- **Local Embedding Generation:** Use the `SentenceTransformers` library (specifically the `all-MiniLM-L6-v2` model) to generate vector embeddings locally within the backend.
- **Real-time Synchronization:** Vector embeddings must be generated and stored automatically whenever a product is created or updated in the database.
- **Natural Language Product Discovery:** Integrate the semantic search results into the agent's response logic, allowing it to recommend products naturally.

## Technical Requirements
- **Vector Storage:** Enable and use the `pgvector` extension in PostgreSQL to store and query product embeddings.
- **Backend Integration:**
  - Add `sentence-transformers` and `torch` (CPU version) to backend dependencies.
  - Implement a dedicated service or utility for embedding generation.
  - Modify the `Product` model to include an `embedding` column (Vector type).
- **Search Logic:** Implement a `search_products_semantic` tool for the LangChain agent that performs vector similarity search.

## Acceptance Criteria
- [ ] Products in the database have associated vector embeddings.
- [ ] New/Updated products automatically trigger embedding generation.
- [ ] The agent correctly retrieves relevant products for semantic queries (e.g., "Recommend some athletic wear") and includes them in the chat.
- [ ] No significant performance degradation in standard database operations.

## Out of Scope
- Multi-modal RAG (e.g., searching by images).
- User-specific personalization within the RAG context (this is a separate track).
- Advanced re-ranking of search results.
