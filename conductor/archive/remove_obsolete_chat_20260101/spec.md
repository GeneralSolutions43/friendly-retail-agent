# Spec: Remove Obsolete Original Chat Interface

## Overview
The original chat interface implemented in the `Home` page is no longer needed since the introduction of the `MinimalAgentOverlay`. This track involves removing the obsolete components and logic from the `Home` page and deleting the unneeded component files.

## Functional Requirements
- **Simplify Home Page:** Remove the chat logic, `MessageList`, and `ChatInput` from `frontend/src/app/page.tsx`.
- **Cleanup Components:** Delete the following files from `frontend/src/components/`:
    - `ChatInput.tsx`
    - `ChatInput.test.tsx`
    - `MessageList.tsx`
    - `MessageList.test.tsx`
- **Maintain Overlay:** Ensure `MinimalAgentOverlay` continues to function correctly as it is integrated via `RootLayout`.

## Acceptance Criteria
- [ ] `frontend/src/app/page.tsx` is simplified and contains no chat-related logic or imports.
- [ ] Obsolete component and test files are deleted.
- [ ] The application builds and runs without errors.
- [ ] The `MinimalAgentOverlay` is still visible and functional on the home page.

## Out of Scope
- Modifying the `RootLayout` or `MinimalAgentOverlay` logic.
- Adding new features to the landing page.
