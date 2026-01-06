"""Main entry point for the FastAPI backend application."""

import os
from typing import List, Generator, Literal
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select, create_engine, SQLModel
from pydantic import BaseModel
from .models import Product


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL)


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Create database tables on startup."""
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)

# CORS Configuration
origins = [
    "http://localhost:3002",
    "http://localhost:3000",
    "http://127.0.0.1:3002",
    "http://127.0.0.1:3000",
    "http://77.42.45.39:3002",
    "http://77.42.45.39:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""

    message: str
    tone: Literal["Helpful Professional", "Friendly Assistant", "Expert Consultant"]


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""

    response: str
    tone: str


def get_session() -> Generator[Session, None, None]:
    """Dependency to get a database session."""
    with Session(engine) as session:
        yield session


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Check the health status of the application.

    Returns:
        dict: A dictionary containing the status of the application.
    """
    return {"status": "ok"}


@app.get("/products", response_model=List[Product])
def list_products(session: Session = Depends(get_session)) -> List[Product]:
    """List all products.

    Args:
        session (Session): The database session.

    Returns:
        List[Product]: A list of all products.
    """
    statement = select(Product)
    products = session.exec(statement).all()
    return products


@app.get("/products/search", response_model=List[Product])
def search_products(
    query: str = Query(..., min_length=1), session: Session = Depends(get_session)
) -> List[Product]:
    """Search for products by name or description.

    Args:
        query (str): The search query string.
        session (Session): The database session.

    Returns:
        List[Product]: A list of products matching the query.
    """
    statement = select(Product).where(
        (Product.name.contains(query)) | (Product.description.contains(query))
    )
    products = session.exec(statement).all()
    return products


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    """Handle chat messages with configurable personality/tone.

    Args:
        request (ChatRequest): The incoming chat request.

    Returns:
        ChatResponse: The agent's response.
    """
    # Mocked logic for now
    if request.tone == "Helpful Professional":
        response_text = (
            f"I have received your message: '{request.message}'. "
            "How may I assist you further?"
        )
    elif request.tone == "Friendly Assistant":
        response_text = (
            f"Hey there! Got your message: '{request.message}'. "
            "Let me know what you need!"
        )
    else:  # Expert Consultant
        response_text = (
            f"I have analyzed your input: '{request.message}'. "
            "Here are my recommendations."
        )

    return ChatResponse(response=response_text, tone=request.tone)
