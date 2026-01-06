import numpy as np
import pytest
from pydantic import BaseModel, TypeAdapter
from typing import Any

class GenericModel(BaseModel):
    data: Any

def test_numpy_serialization_error():
    """
    Test that a generic Pydantic model fails to serialize a numpy array by default.
    """
    model = GenericModel(data=np.array([1, 2, 3]))
    
    # This should fail initially
    with pytest.raises(Exception) as excinfo:
        model.model_dump_json()
    
    # In Pydantic v2, it's PydanticSerializationError
    assert "Unable to serialize unknown type: <class 'numpy.ndarray'>" in str(excinfo.value)

def test_numpy_list_serialization():
    """
    Test serialization of a list containing numpy arrays if we have a global handler.
    (This will fail until the fix is implemented)
    """
    data = {"items": [np.array([1.0, 2.0]), np.array([3.0, 4.0])]}
    adapter = TypeAdapter(dict[str, list[Any]])
    
    with pytest.raises(Exception):
        adapter.dump_json(data)
