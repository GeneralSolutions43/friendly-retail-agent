# Specification: AI Agent Memory (Conversation History)

## Overview
This track implements session-based conversation history for the Friendly Retail Agent. By integrating Redis as a storage backend, the agent will support multi-turn conversations, maintaining context across multiple user inputs. This enables more natural interactions, such as following up on previous product searches or remembering user preferences within a session.

## User Stories
- As a shopper, I want the agent to remember my previous questions so I don't have to repeat myself.
- As a shopper, I want to use pronouns like "it" or "them" to refer to products we just discussed.
- As a shopper, I want the agent's tone and greeting to remain consistent and context-aware throughout our session.

## Functional Requirements
### 1. Session Management
- **Session Identification:** The frontend will generate a unique `sessionId` (UUID) upon the first interaction and persist it in `localStorage`.
- **Session Persistence:** The `sessionId` must be included in all chat requests to the backend.

### 2. Backend Memory Storage (Redis)
- **Redis Integration:** Add a Redis service to `docker-compose.yml`.
- **Message Storage:** Store conversation history in Redis indexed by `sessionId`.
- **Summary Memory:** Implement a summarization logic (using the LLM) to compress long conversation histories, preventing context window overflow while retaining key information (preferences, previous products).

### 3. Multi-turn AI Logic
- **Context Injection:** The backend will retrieve and inject the (summarized) conversation history into the LLM prompt for each request.
- **Contextual Awareness:** The agent should specifically prioritize:
    - Past product preferences (colors, budget, categories).
    - Contextual follow-ups (referencing previous entities).
    - Greeting state (avoiding repeated introductions).
    - Tone consistency.

### 4. Frontend Integration
- **Session ID Handling:** Generate and store `sessionId` if not present.
- **Request Update:** Update `/chat` and `/chat/stream` endpoints to accept `sessionId`.

## Non-Functional Requirements
- **Performance:** Retrieving memory from Redis should add minimal latency (<50ms).
- **Scalability:** Summarization should happen asynchronously or efficiently to avoid blocking the main chat response.
- **Reliability:** If Redis is unavailable, the agent should gracefully degrade to single-turn mode.

## Acceptance Criteria
- [ ] Redis service is running and accessible by the backend.
- [ ] Multiple messages in a session result in the agent acknowledging previous context.
- [ ] Refreshing the page persists the conversation history (retrieved upon the first new message).
- [ ] Conversation summaries are generated when history exceeds a certain length/token count.
- [ ] Unit tests verify memory retrieval and injection logic.

## Out of Scope
- User accounts and cross-device synchronization (this is session-based, not user-based).
- Long-term memory across different sessions (e.g., remembering preferences from a week ago).
