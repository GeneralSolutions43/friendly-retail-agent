import os
import logging
from typing import List
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_groq import ChatGroq

logger = logging.getLogger(__name__)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def summarize_messages(messages: List[BaseMessage]) -> str:
    """
    Summarize a list of messages into a concise summary of the conversation state.
    """
    if not messages:
        return ""
        
    if not GROQ_API_KEY:
        logger.warning("GROQ_API_KEY not found. Skipping summarization.")
        return "History summary unavailable (missing API key)."
        
    logger.info(f"Summarizing {len(messages)} messages...")
    
    llm = ChatGroq(model="openai/gpt-oss-120b", api_key=GROQ_API_KEY, temperature=0)
    
    # Format messages for the summarization prompt
    formatted_history = ""
    for msg in messages:
        role = "User" if isinstance(msg, HumanMessage) else "Assistant"
        formatted_history += f"{role}: {msg.content}\n"
        
    prompt = [
        SystemMessage(content="You are an expert at summarizing retail conversations. Provide a concise summary of the key points, user preferences, and items discussed. Focus on what is relevant for a retail assistant to remember."),
        HumanMessage(content=f"Please summarize the following conversation history:\n\n{formatted_history}")
    ]
    
    try:
        response = llm.invoke(prompt)
        summary = str(response.content)
        logger.info(f"Summary generated: {summary[:100]}...")
        return summary
    except Exception as e:
        logger.error(f"Error during summarization: {e}")
        return "Error generating conversation summary."
