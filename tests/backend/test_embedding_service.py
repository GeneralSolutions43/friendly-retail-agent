import pytest
from app.embeddings import get_embedding

def test_get_embedding_returns_vector():
    text = "This is a test product description."
    embedding = get_embedding(text)
    
    assert isinstance(embedding, list)
    assert len(embedding) == 384
    assert isinstance(embedding[0], float)

def test_get_embedding_consistency():
    text = "Consistent text"
    emb1 = get_embedding(text)
    emb2 = get_embedding(text)
    assert emb1 == emb2
