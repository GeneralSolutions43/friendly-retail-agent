# Plan: AI Integration with Llama 3 and Tool Calling

## Phase 1: Environment & SDK Setup
- [x] Task: Install Groq dependencies f30c157
    - [ ] Implement Feature: Add `groq` and `langchain-groq` to `backend/pyproject.toml`
- [x] Task: Configure API Key management 4c042da
    - [ ] Implement Feature: Update `backend/app/main.py` to load `GROQ_API_KEY` from environment
- [ ] Task: Conductor - User Manual Verification 'Environment & SDK Setup' (Protocol in workflow.md)

## Phase 2: Agent & Tool Logic [checkpoint: 3ebb106]
- [x] Task: Define Product Search Tool 3ebb106
    - [x] Write Tests: Verify the tool correctly wraps the `search_products` database logic
    - [x] Implement Feature: Create a LangChain tool for product search
- [x] Task: Implement Agent with Dynamic System Prompts 3ebb106
    - [x] Write Tests: Verify the agent correctly selects prompts based on 'tone'
    - [x] Implement Feature: Create the agent executor logic in the backend
- [x] Task: Conductor - User Manual Verification 'Agent & Tool Logic' (Protocol in workflow.md)

## Phase 3: API Integration
- [ ] Task: Update Chat Endpoint to use Agent
    - [ ] Write Tests: Verify `/chat` returns AI-generated responses (can use mock for API call)
    - [ ] Implement Feature: Replace mock logic in `POST /chat` with the agent call
- [ ] Task: Conductor - User Manual Verification 'API Integration' (Protocol in workflow.md)
