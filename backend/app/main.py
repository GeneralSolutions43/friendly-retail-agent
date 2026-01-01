"""Main entry point for the FastAPI backend application."""

from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Check the health status of the application.

    Returns:
        dict: A dictionary containing the status of the application.
    """
    return {"status": "ok"}
