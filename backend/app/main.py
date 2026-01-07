"Main entry point for the FastAPI backend application."

import os
import json
import logging
from typing import List, Generator, Literal, Any
from contextlib import asynccontextmanager
import numpy as np
from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from fastapi.responses import JSONResponse
from fastapi.encoders import ENCODERS_BY_TYPE
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select, create_engine, SQLModel, text
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from .models import Product
from .embeddings import get_embedding

# Register numpy array encoder for FastAPI's jsonable_encoder
ENCODERS_BY_TYPE[np.ndarray] = lambda x: x.tolist()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("WARNING: GROQ_API_KEY not found in environment. AI features will fail.")


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Create database tables on startup."""
    with Session(engine) as session:
        session.exec(text("CREATE EXTENSION IF NOT EXISTS vector"))
        session.commit()
    SQLModel.metadata.create_all(engine)
    yield


class NumpyJSONResponse(JSONResponse):
    """Custom JSONResponse that handles numpy arrays by converting them to lists."""

    def render(self, content: Any) -> bytes:
        def numpy_default(obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return str(obj)

        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=( ",", ":"),
            default=numpy_default,
        ).encode("utf-8")


app = FastAPI(lifespan=lifespan, default_response_class=NumpyJSONResponse)

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


@tool
def search_products_semantic(query: str) -> str:
    """Search for products using semantic vector similarity.

    Use this tool when the user's query implies a meaning, theme, need, or problem (e.g., 'sore muscles', 'gift for runner', 'winter gear') rather than specific keywords.
    
    Args:
        query: The search text to find semantically similar products for.
    """
    embedding_vector = get_embedding(query)

    with Session(engine) as session:
        # Order by similarity (L2 distance)
        statement = select(Product).order_by(
            Product.embedding.l2_distance(embedding_vector)  # type: ignore
        ).limit(5)
        products = session.exec(statement).all()

        if not products:
            return f"No relevant products found for '{query}'."

        result = "Found the following relevant products:\n"
        for p in products:
            result += f"- {p.name} ({p.category}): ${p.price}. {p.description}\n"
        return result

def get_agent_response(message: str, tone: str) -> str:
    """Invoke the AI agent and return the response text."""
    logger.info(f"Generating agent response for message: '{message}' with tone: '{tone}'")
    llm = ChatGroq(model="openai/gpt-oss-120b", api_key=GROQ_API_KEY, temperature=0.7)

    tools = [search_products_tool, search_products_semantic]
    llm_with_tools = llm.bind_tools(tools)

    system_prompts = {
        "Helpful Professional": (
            "You are a helpful and professional retail assistant. "
            "Provide clear, concise, and accurate information. "
            "Use the available tools to search for product details. "
            "Always acknowledge the user's input and provide a helpful response, even if no products are found or searched."
        ),
        "Friendly Assistant": (
            "You are a super friendly and enthusiastic retail assistant! "
            "Use emojis, be warm, and make the customer feel excited about their shopping journey. "
            "Always check our product catalog using tools if needed. "
            "Even if you don't find a product, always chat back and acknowledge what the user said with enthusiasm!"
        ),
        "Expert Consultant": (
            "You are a highly knowledgeable retail expert and consultant. "
            "Provide deep insights, detailed product comparisons, and curated advice. "
            "Analyze product data from the tools carefully before responding. "
            "Always provide a thoughtful acknowledgment of the user's statements or preferences."
        ),
    }

    messages = [
        SystemMessage(
            content=system_prompts.get(tone, system_prompts["Helpful Professional"])
        ),
        HumanMessage(content=message),
    ]

    ai_msg = llm_with_tools.invoke(messages)
    logger.info(f"Initial AI message received: {ai_msg}")
    messages.append(ai_msg)

    # Process tool calls
    for tool_call in ai_msg.tool_calls:
        selected_tool_map = {
            "search_products_tool": search_products_tool,
            "search_products_semantic": search_products_semantic,
        }
        selected_tool = selected_tool_map.get(tool_call["name"].lower())
        if selected_tool:
            logger.info(f"Invoking tool: {tool_call['name']} with args: {tool_call['args']}")
            tool_output = selected_tool.invoke(tool_call["args"])
            logger.info(f"Tool output: {tool_output}")
            messages.append(ToolMessage(tool_output, tool_call_id=tool_call["id"]))

    content = ""
    if ai_msg.tool_calls:
        # Get final response after tool outputs
        final_msg = llm_with_tools.invoke(messages)
        logger.info(f"Final AI message received: {final_msg}")
        content = str(final_msg.content)
    else:
        content = str(ai_msg.content)

    if not content or content.strip() == "":
        logger.warning(f"AI returned an empty response for message: '{message}'")
        raise ValueError("AI generated an empty response.")

    return content


async def get_streaming_agent_response(message: str, tone: str) -> Generator[str, None, None]:
    """Invoke the AI agent and stream the response tokens."""
    logger.info(f"Generating streaming agent response for message: '{message}' with tone: '{tone}'")
    llm = ChatGroq(model="openai/gpt-oss-120b", api_key=GROQ_API_KEY, temperature=0.7)

    tools = [search_products_tool, search_products_semantic]
    llm_with_tools = llm.bind_tools(tools)

    system_prompts = {
        "Helpful Professional": (
            "You are a helpful and professional retail assistant. "
            "Provide clear, concise, and accurate information. "
            "Use the available tools to search for product details. "
            "Always acknowledge the user's input and provide a helpful response, even if no products are found or searched."
        ),
        "Friendly Assistant": (
            "You are a super friendly and enthusiastic retail assistant! "
            "Use emojis, be warm, and make the customer feel excited about their shopping journey. "
            "Always check our product catalog using tools if needed. "
            "Even if you don't find a product, always chat back and acknowledge what the user said with enthusiasm!"
        ),
        "Expert Consultant": (
            "You are a highly knowledgeable retail expert and consultant. "
            "Provide deep insights, detailed product comparisons, and curated advice. "
            "Analyze product data from the tools carefully before responding. "
            "Always provide a thoughtful acknowledgment of the user's statements or preferences."
        ),
    }

    messages = [
        SystemMessage(
            content=system_prompts.get(tone, system_prompts["Helpful Professional"])
        ),
        HumanMessage(content=message),
    ]

    # First turn streaming
    collected_ai_message = None
    has_content = False

    async for chunk in llm_with_tools.astream(messages):
        if collected_ai_message is None:
            collected_ai_message = chunk
        else:
            collected_ai_message += chunk
        
        if chunk.content:
            has_content = True
            yield f"data: {json.dumps({'response': chunk.content, 'tone': tone})}\n\n"

    messages.append(collected_ai_message)

    if collected_ai_message.tool_calls:
        # Process tool calls
        for tool_call in collected_ai_message.tool_calls:
            selected_tool_map = {
                "search_products_tool": search_products_tool,
                "search_products_semantic": search_products_semantic,
            }
            selected_tool = selected_tool_map.get(tool_call["name"].lower())
            if selected_tool:
                logger.info(f"Invoking tool: {tool_call['name']} with args: {tool_call['args']}")
                tool_output = selected_tool.invoke(tool_call["args"])
                logger.info(f"Tool output: {tool_output}")
                messages.append(ToolMessage(tool_output, tool_call_id=tool_call["id"]))
        
        # Stream final response after tools
        async for chunk in llm_with_tools.astream(messages):
            if chunk.content:
                has_content = True
                yield f"data: {json.dumps({'response': chunk.content, 'tone': tone})}\n\n"
    
    if not has_content:
        yield f"data: {json.dumps({'response': 'I encountered an issue processing that. Could you try rephrasing?', 'tone': tone})}\n\n"


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
    try:
        response_text = get_agent_response(request.message, request.tone)
    except ValueError as e:
        logger.error(f"Error in chat_endpoint: {e}")
        response_text = "I'm sorry, I encountered an issue processing that. Could you try rephrasing?"
    
    return ChatResponse(response=response_text, tone=request.tone)


@app.post("/chat/stream")
async def chat_stream_endpoint(request: ChatRequest):
    """Handle chat messages with streaming response."""
    return StreamingResponse(
        get_streaming_agent_response(request.message, request.tone),
        media_type="text/event-stream"
    )
