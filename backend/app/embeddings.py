from sentence_transformers import SentenceTransformer
from typing import List

_model = None

def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        # Use CPU for compatibility and lower resource usage in this env
        _model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
    return _model

def get_embedding(text: str) -> List[float]:
    """Generates a vector embedding for the given text using a local model."""
    model = get_model()
    # encode returns a numpy array, convert to standard list of floats
    embedding = model.encode(text).tolist()
    return embedding
