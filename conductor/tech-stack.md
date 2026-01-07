# Tech Stack - Friendly Retail Agent

## Frontend
* **Framework:** Next.js (React-based)
* **Language:** TypeScript
* **Styling:** Tailwind CSS (Inferred for a modern, minimalist design)

## Backend
* **Framework:** FastAPI
* **Communication:** Server-Sent Events (SSE) for real-time streaming.
* **Language:** Python
* **AI/ML Integration:** Llama 3 via Groq API, LangChain for agent and tool management.
* **Vector Search:** pgvector (PostgreSQL extension), SentenceTransformers (all-MiniLM-L6-v2) for local embedding generation.

## Database & Storage
* **Primary Database:** PostgreSQL (for structured product and user data)
* **Caching/Sessions:** Redis (Implemented for session-based conversation history and persistence)

## Deployment & Infrastructure (Inferred)
* **Containerization:** Docker
