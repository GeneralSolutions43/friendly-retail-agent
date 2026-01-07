# Plan: AI Agent Memory (Conversation History)

## Phase 1: Infrastructure & Redis Setup
- [x] Task: Add Redis service to `docker-compose.yml` ca18ca3
- [x] Task: Update `backend/requirements.txt` with `redis` and `langchain-redis` (if needed) 764fe34
- [ ] Task: Create a basic Redis connection utility in the backend
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Infrastructure & Redis Setup' (Protocol in workflow.md)

## Phase 2: Backend - Basic Session Storage
- [ ] Task: Update `ChatRequest` model to include `session_id`
- [ ] Task: Implement `RedisChatMessageHistory` integration in `backend/app/main.py`
- [ ] Task: Update `get_agent_response` to retrieve and use message history
- [ ] Task: Update `get_streaming_agent_response` to retrieve and use message history
- [ ] Task: Add unit tests for session-based message retrieval
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Backend - Basic Session Storage' (Protocol in workflow.md)

## Phase 3: Backend - Summarization Logic
- [ ] Task: Implement summarization utility using LangChain's `ConversationSummaryBufferMemory` or equivalent logic
- [ ] Task: Integrate summarization into the chat endpoints to handle long histories
- [ ] Task: Add unit tests for summarization triggers and content retention
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Backend - Summarization Logic' (Protocol in workflow.md)

## Phase 4: Frontend Integration
- [ ] Task: Implement `sessionId` generation and `localStorage` persistence in the frontend
- [ ] Task: Update frontend API calls to include `sessionId` in chat requests
- [ ] Task: Verify that refreshing the page maintains the session context in the UI (agent continues the conversation)
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Frontend Integration' (Protocol in workflow.md)

## Phase 5: Final Verification & Polishing
- [ ] Task: Perform end-to-end testing of multi-turn conversations
- [ ] Task: Verify memory persistence across restarts (if Redis volume is configured)
- [ ] Task: Final code cleanup and documentation update
- [ ] Task: Conductor - User Manual Verification 'Phase 5: Final Verification & Polishing' (Protocol in workflow.md)
