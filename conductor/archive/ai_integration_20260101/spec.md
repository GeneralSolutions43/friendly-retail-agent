# Spec: AI Integration with Llama 3 and Tool Calling

## Overview
Replace the mocked chat logic with a functional AI agent powered by Llama 3 via the Groq API. The agent will support tool calling to interact with the existing project database (e.g., searching for products) and will dynamically adapt its tone based on user configuration.

## Functional Requirements
- **Groq API Integration:** Connect the FastAPI backend to the Groq Cloud API.
- **Dynamic Personas:** Implement system prompts for "Helpful Professional", "Friendly Assistant", and "Expert Consultant" tones.
- **Tool Calling (Function Calling):**
    - The agent should be able to call the `list_products` or `search_products` logic as a tool.
    - When a user asks about product availability or recommendations, the agent must fetch data from the database before responding.
- **Streaming (Optional):** Initial implementation will focus on complete responses, with hooks for future streaming support.

## Technical Requirements
- **Library:** Use `langchain-groq` or the raw `groq` Python SDK.
- **Environment Variables:** Require `GROQ_API_KEY` in the backend environment.
- **FastAPI Updates:** Update the `/chat` endpoint to invoke the AI logic instead of returning mocks.

## Acceptance Criteria
- [ ] Agent correctly identifies when to use the `search_products` tool based on user queries.
- [ ] Responses from the agent reflect the selected tone (e.g., more enthusiastic for "Friendly Assistant").
- [ ] Database data is accurately represented in the agent's natural language responses.
- [ ] The system handles missing API keys or network errors gracefully.

## Out of Scope
- Complex multi-turn state persistence (initially focusing on single-turn context or basic history).
- Fine-tuning the model.
