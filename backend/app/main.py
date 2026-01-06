"Main entry point for the FastAPI backend application."

import os
import json
from typing import List, Generator, Literal
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select, create_engine, SQLModel
from pydantic import BaseModel
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from .models import Product


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("WARNING: GROQ_API_KEY not found in environment. AI features will fail.")


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


@tool
def search_products_tool(query: str) -> str:
    """Search for products in the retail store by name or description.

    Args:
        query: The search term to look for.
    """
    with Session(engine) as session:
        statement = select(Product).where(
            (Product.name.contains(query)) | (Product.description.contains(query))
        )
        products = session.exec(statement).all()
        if not products:
            return f"No products found matching '{query}'."

        result = "Found the following products:\n"
        for p in products:
            result += f"- {p.name} ({p.category}): ${p.price}. {p.description}\n"
        return result


def get_agent_response(message: str, tone: str) -> str:
    """Invoke the AI agent and return the response text."""
    llm = ChatGroq(model="openai/gpt-oss-120b", api_key=GROQ_API_KEY, temperature=0.7)

    tools = [search_products_tool]
    llm_with_tools = llm.bind_tools(tools)

    system_prompts = {
        "Helpful Professional": (
            "You are a helpful and professional retail assistant. "
            "Provide clear, concise, and accurate information. "
            "Use the available tools to search for product details."
        ),
        "Friendly Assistant": (
            "You are a super friendly and enthusiastic retail assistant! "
            "Use emojis, be warm, and make the customer feel excited about their shopping journey. "
            "Always check our product catalog using tools if needed."
        ),
        "Expert Consultant": (
            "You are a highly knowledgeable retail expert and consultant. "
            "Provide deep insights, detailed product comparisons, and curated advice. "
            "Analyze product data from the tools carefully before responding."
        ),
    }

    messages = [
        SystemMessage(
            content=system_prompts.get(tone, system_prompts["Helpful Professional"])
        ),
        HumanMessage(content=message),
    ]

    ai_msg = llm_with_tools.invoke(messages)
    messages.append(ai_msg)

    # Process tool calls
    for tool_call in ai_msg.tool_calls:
        selected_tool = {"search_products_tool": search_products_tool}[
            tool_call["name"].lower()
        ]
        tool_output = selected_tool.invoke(tool_call["args"])
        messages.append(ToolMessage(tool_output, tool_call_id=tool_call["id"]))

    if ai_msg.tool_calls:
        # Get final response after tool outputs
        final_msg = llm_with_tools.invoke(messages)
        return str(final_msg.content)

    return str(ai_msg.content)


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
    response_text = get_agent_response(request.message, request.tone)
    return ChatResponse(response=response_text, tone=request.tone)

