from unittest.mock import MagicMock, patch
from app.main import get_agent_response

# We mock the tool inside app.main so get_agent_response uses the mock
@patch('app.main.search_products_semantic')
@patch('app.main.ChatGroq')
def test_semantic_search_end_to_end_flow(mock_chat_groq, mock_semantic_tool):
    # Setup mock LLM
    mock_llm = MagicMock()
    mock_chat_groq.return_value = mock_llm
    
    # Mock the bound LLM
    mock_bound_llm = mock_llm.bind_tools.return_value
    
    # Scenario: User asks "I need winter gear"
    # 1. LLM decides to call search_products_semantic
    tool_call_msg = MagicMock()
    tool_call_msg.tool_calls = [{
        "name": "search_products_semantic",
        "args": {"query": "winter gear"},
        "id": "call_123"
    }]
    tool_call_msg.content = ""
    
    # 2. Tool is executed (we mock the return value)
    mock_semantic_tool.invoke.return_value = "Found: Winter Jacket ($100)"
    
    # 3. LLM receives tool output and generates final response
    final_msg = MagicMock()
    final_msg.content = "I found a Winter Jacket for you that costs $100."
    final_msg.tool_calls = []
    
    # Set side_effect for the sequence of calls
    # first call -> tool_call_msg
    # second call -> final_msg
    mock_bound_llm.invoke.side_effect = [tool_call_msg, final_msg]
    
    response = get_agent_response("I need winter gear", "Friendly Assistant")
    
    # Assertions
    assert "Winter Jacket" in response
    mock_semantic_tool.invoke.assert_called_with({"query": "winter gear"})
    
    # Verify the LLM was called with tool messages
    assert mock_bound_llm.invoke.call_count == 2
