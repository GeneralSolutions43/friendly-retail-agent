# Plan: Streaming AI Responses

This plan outlines the implementation of real-time token streaming for the Friendly Retail Agent, covering both backend SSE delivery and frontend incremental rendering.

## Phase 1: Backend SSE Implementation
Goal: Enable the FastAPI backend to stream AI-generated tokens using Server-Sent Events (SSE).

- [x] Task: Backend - Implement Streaming Endpoint (3f34685)
    - [ ] Sub-task: Write unit tests for a new `/chat/stream` endpoint that mocks SSE output.
    - [ ] Sub-task: Implement the `/chat/stream` endpoint in `backend/app/main.py` using FastAPI's `StreamingResponse`.
    - [ ] Sub-task: Configure LangChain/ChatGroq to use `.astream()` for token generation.
- [ ] Task: Conductor - User Manual Verification 'Backend SSE Implementation' (Protocol in workflow.md)

## Phase 2: Frontend Streaming Integration
Goal: Update the Next.js frontend to consume the SSE stream and update the chat UI in real-time.

- [ ] Task: Frontend - Consumer Stream Reader
    - [ ] Sub-task: Write unit tests for the streaming message handler (mocking a `ReadableStream`).
    - [ ] Sub-task: Update `handleSendMessage` in `MinimalAgentOverlay.tsx` to use the Fetch API's `body.getReader()` to consume tokens.
- [ ] Task: Conductor - User Manual Verification 'Frontend Streaming Integration' (Protocol in workflow.md)

## Phase 3: UX Polishing & Auto-scroll
Goal: Refine the user experience with typing indicators and seamless scrolling during streaming.

- [ ] Task: Frontend - UI/UX Refinement
    - [ ] Sub-task: Add a `isStreaming` state and a "Typing..." indicator to the chat overlay.
    - [ ] Sub-task: Implement auto-scroll logic to keep the newest tokens in view during the stream.
    - [ ] Sub-task: Verify responsive behavior and smooth transitions on both mobile and desktop views.
- [ ] Task: Conductor - User Manual Verification 'UX Polishing & Auto-scroll' (Protocol in workflow.md)

## Phase 4: Final Verification
Goal: Ensure the end-to-end flow meets all acceptance criteria and quality gates.

- [ ] Task: End-to-End Verification
    - [ ] Sub-task: Verify all personas correctly apply their tone to the stream.
    - [ ] Sub-task: Check that the stream handles network interruptions gracefully.
- [ ] Task: Conductor - User Manual Verification 'Final Verification' (Protocol in workflow.md)
