import pytest
from unittest.mock import patch, MagicMock

# We need to import the tool. It's not created yet, so this import will fail (RED)
# We assume it will be in app.main
from app.main import search_products_semantic

@patch("app.main.get_embedding")
@patch("app.main.Session")
@patch("app.main.engine")
def test_semantic_search_tool_logic(mock_engine, mock_session_cls, mock_get_embedding):
    # Setup mocks
    mock_get_embedding.return_value = [0.1] * 384
    
    mock_session = mock_session_cls.return_value.__enter__.return_value
    
    # Mock product result
    mock_product = MagicMock()
    mock_product.name = "Test Product"
    mock_product.category = "Test"
    mock_product.price = 10.0
    mock_product.description = "Desc"
    
    # exec().all() returns list of products
    mock_session.exec.return_value.all.return_value = [mock_product]
    
    # Execute tool
    result = search_products_semantic.invoke({"query": "winter clothes"})
    
    # Assertions
    mock_get_embedding.assert_called_with("winter clothes")
    assert "Test Product" in result
    assert "winter clothes" not in result # The tool shouldn't just echo the query, but results.
    
    # Check format: "- Name (Category): $Price. Description"
    assert "- Test Product (Test): $10.0. Desc" in result
    
    # Check that session.exec was called
    mock_session.exec.assert_called()
