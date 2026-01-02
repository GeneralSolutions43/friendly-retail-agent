# Spec: Fix CORS Error in Chat Communication

## Overview
The frontend application is unable to communicate with the backend API when running in Docker, resulting in a "Failed to fetch" error. This is caused by the lack of Cross-Origin Resource Sharing (CORS) configuration in the FastAPI backend, which blocks requests from the frontend origin (http://localhost:3002).

## Functional Requirements
- **Enable CORS:** The FastAPI backend must be configured to accept requests from the frontend application.
- **Allowed Origins:** Specifically allow `http://localhost:3002` (and potentially `http://localhost:3000` or `*` for development flexibility).
- **Allowed Methods/Headers:** Allow standard methods (GET, POST, OPTIONS) and headers.

## Acceptance Criteria
- [ ] The `CORSMiddleware` is correctly added to `backend/app/main.py`.
- [ ] Frontend can successfully send a message to `/chat` without a "Failed to fetch" error in the Docker environment.
- [ ] Health check and Search endpoints also work from the frontend.

## Out of Scope
- configuring strict CORS for production domain (this is for the dev/docker fix).
