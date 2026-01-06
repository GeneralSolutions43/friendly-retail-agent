# Plan: Fix Product Serialization Error (numpy.ndarray)

## Phase 1: Reproduction and Base Testing [checkpoint: 6ffc9c1]
- [x] Task: Create a failing test case in `tests/backend/test_products.py` that reproduces the 500 error on `GET /products`. 3268366
- [x] Task: Create a new test file `tests/backend/test_serialization.py` to test generic `numpy.ndarray` serialization in Pydantic models. 3268366
- [x] Task: Run tests and confirm they fail with `PydanticSerializationError`. 3268366
- [x] Task: Conductor - User Manual Verification 'Phase 1: Reproduction and Base Testing' (Protocol in workflow.md) 3268366

## Phase 2: Implementation of Fixes [checkpoint: f7db152]
- [x] Task: Update `backend/app/models.py` to exclude the `embedding` field from serialization in the `Product` model. 4bf7fdc
- [x] Task: Implement a global serialization handler for `numpy.ndarray` in `backend/app/main.py` (e.g., using a custom FastAPI `DefaultJSONResponse` or Pydantic configuration). 4bf7fdc
- [x] Task: Run tests to ensure `GET /products` returns 200 OK and excludes the `embedding` field. 4bf7fdc
- [x] Task: Run generic serialization tests to ensure `numpy.ndarray` is now handled correctly. 4bf7fdc
- [x] Task: Conductor - User Manual Verification 'Phase 2: Implementation of Fixes' (Protocol in workflow.md) 4bf7fdc

## Phase 3: Final Verification and Quality Gates
- [x] Task: Verify `GET /products/search` also works correctly and excludes embeddings. 2d3eb16
- [x] Task: Run full backend test suite to ensure no regressions. 2d3eb16
- [x] Task: Run coverage reports using the project's chosen tools. For example, in a Python project, this might look like: 2d3eb16
- [x] Task: Verify code coverage for modified files is >80%. 2d3eb16
- [x] Task: Run linting and type checking (`ruff`, `mypy` or `pyright`). 2d3eb16
- [x] Task: Conductor - User Manual Verification 'Phase 3: Final Verification and Quality Gates' (Protocol in workflow.md) 2d3eb16
