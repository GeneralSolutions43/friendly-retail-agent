import numpy as np
import pytest
from pydantic import BaseModel, TypeAdapter
from typing import Any

class GenericModel(BaseModel):
    data: Any

def test_numpy_serialization_success():
    """
    Test that a numpy array can be serialized when using the custom response logic.
    """
    from backend.app.main import NumpyJSONResponse
    import json
    
    data = {"array": np.array([1, 2, 3])}
    response = NumpyJSONResponse(content=data)
    rendered = json.loads(response.body.decode())
    assert rendered["array"] == [1, 2, 3]

def test_numpy_list_serialization_success():
    """
    Test serialization of a list containing numpy arrays using the custom response class.
    """
    from backend.app.main import NumpyJSONResponse
    import json
    
    data = {"items": [np.array([1.0, 2.0]), np.array([3.0, 4.0])]}
    response = NumpyJSONResponse(content=data)
    rendered = json.loads(response.body.decode())
    assert rendered["items"] == [[1.0, 2.0], [3.0, 4.0]]
