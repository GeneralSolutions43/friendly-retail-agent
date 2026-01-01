"""Main entry point for the FastAPI backend application."""

import os
from typing import List, Generator
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Query
from sqlmodel import Session, select, create_engine, SQLModel
from backend.app.models import Product


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL)


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Create database tables on startup."""
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)


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


@app.get("/products/search", response_model=List[Product])
def search_products(
    query: str = Query(..., min_length=1),
    session: Session = Depends(get_session)
) -> List[Product]:
    """Search for products by name or description.

    Args:
        query (str): The search query string.
        session (Session): The database session.

    Returns:
        List[Product]: A list of products matching the query.
    """
    statement = select(Product).where(
        (Product.name.contains(query)) |
        (Product.description.contains(query))
    )
    products = session.exec(statement).all()
    return products
