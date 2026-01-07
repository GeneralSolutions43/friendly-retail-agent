# Specification: Fix Product Serialization Error (numpy.ndarray)

## Overview
The `GET /products` endpoint currently returns an "Internal Server Error" (500) because the `Product` model includes an `embedding` field (stored as a vector). When retrieved from the database, this field can be returned as a `numpy.ndarray`, which Pydantic cannot serialize by default.

## Functional Requirements
1.  **Exclude Embedding from API:** Modify the `Product` model to ensure the `embedding` field is excluded from all API responses (serialization).
2.  **Global Numpy Serialization:** Implement a global serialization handler for `numpy.ndarray` to prevent similar crashes if numpy data is encountered in other parts of the system.
3.  **Endpoint Stability:** Ensure `GET /products`, `GET /products/search`, and any other product-returning endpoints return 200 OK.

## Non-Functional Requirements
- **Performance:** Serialization should remain efficient.
- **Robustness:** The system should handle numpy types gracefully rather than crashing.

## Acceptance Criteria
- `GET /products` returns a 200 OK response.
- Product objects in the API response do NOT contain the `embedding` key.
- A test case specifically using a `numpy.ndarray` in a response model passes without serialization errors.

## Out of Scope
- Refactoring to a separate `ProductRead` schema (as per user preference for field-level exclusion).
- Modifying the underlying database schema or vector storage logic.
