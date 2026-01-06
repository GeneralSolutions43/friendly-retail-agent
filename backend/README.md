# Friendly Retail Agent - Backend

This is the backend for the Friendly Retail Agent, built with [FastAPI](https://fastapi.tiangolo.com/). It provides a REST API for product discovery and an intelligent AI agent powered by Llama 3.

## Features

- **AI Agent Integration:** Functional conversational agent using Llama 3 via the Groq API.
- **Tool Calling:** The agent can search the product database in real-time to answer user queries.
- **Dynamic Personas:** Support for multiple agent tones (Professional, Friendly, Expert).
- **Product Management:** REST endpoints for listing and searching products using [SQLModel](https://sqlmodel.tiangolo.com/).
- **CORS Support:** Configured for seamless communication with the frontend.

## Tech Stack

- **Framework:** FastAPI
- **Language:** Python 3.12+
- **Dependency Management:** [uv](https://github.com/astral-sh/uv)
- **Database:** PostgreSQL (with SQLModel ORM)
- **AI/ML:** LangChain, Groq SDK (Llama 3 model)

## Getting Started

### Prerequisites

- Python 3.12+
- `uv` installed
- `GROQ_API_KEY` (Get one at [Groq Cloud](https://console.groq.com/))

### Installation

```bash
cd backend
uv sync
```

### Development

Run the FastAPI server:

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
```

The API will be available at `http://localhost:8002`. You can view the automatic documentation at `http://localhost:8002/docs`.

### Database Seeding

To populate the database with initial product data:

```bash
# Inside backend directory
uv run python -m app.seed
```

### Testing

```bash
cd backend
PYTHONPATH=. uv run pytest ../tests/backend/
```

### Linting

```bash
uv run pylint app
```

## Environment Variables

- `GROQ_API_KEY`: Required for AI features.
- `DATABASE_URL`: Connection string for PostgreSQL (defaults to `sqlite:///./test.db` if not provided).
