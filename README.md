# Friendly Retail Agent

A modern e-commerce demo featuring a personalized AI agent. This project combines a FastAPI backend with a Next.js frontend to deliver a high-touch shopping experience.

## Project Structure

- **`/frontend`**: Next.js application with a storefront demo and a floating AI agent overlay.
- **`/backend`**: FastAPI service providing product data and AI agent logic (Llama 3 via Groq).
- **`/conductor`**: Project management and implementation tracks using the Conductor methodology.

## Getting Started with Docker

The easiest way to run the entire stack is using Docker Compose.

### Prerequisites

- Docker and Docker Compose installed.
- A Groq API Key (Get one at [Groq Cloud](https://console.groq.com/)).

### Running the Application

1.  **Clone the repository.**
2.  **Set your API Key:**
    Export the `GROQ_API_KEY` in your terminal or add it to a `.env` file in the root.
    ```bash
    export GROQ_API_KEY=your_groq_api_key_here
    ```
3.  **Launch the services:**
    ```bash
    docker compose up --build
    ```

### Accessing the Services

- **Frontend:** `http://localhost:3002`
- **Backend API:** `http://localhost:8002`
- **API Docs:** `http://localhost:8002/docs`

## Development

For detailed information on developing and testing each service, please refer to their respective READMEs:

- [Frontend README](./frontend/README.md)
- [Backend README](./backend/README.md)

## License

MIT
