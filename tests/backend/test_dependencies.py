import pytest

def test_torch_installed():
    import torch
    assert torch.__version__ is not None

def test_sentence_transformers_installed():
    import sentence_transformers
    assert sentence_transformers.__version__ is not None
