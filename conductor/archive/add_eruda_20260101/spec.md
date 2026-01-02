# Spec: Add Eruda Console for Mobile Debugging

## Overview
This chore involves integrating the Eruda plugin into the Next.js frontend to provide a browser console for mobile debugging. Eruda should only be active and visible during development to avoid performance impact and security concerns in production.

## Functional Requirements
- Initialize Eruda only when `process.env.NODE_ENV === 'development'`.
- Provide a `ErudaProvider` component (or similar) to wrap the application layout or handle initialization.
- Ensure the Eruda "gear" icon appears on mobile browsers (and desktop) during development.

## Non-Functional Requirements
- **Environment Isolation:** Eruda must not be bundled or executed in production builds.
- **Performance:** Initialization should be deferred or handled efficiently to minimize impact on development boot times.

## Acceptance Criteria
- [ ] Eruda is accessible in the browser when running `npm run dev`.
- [ ] Eruda is NOT accessible when running in production mode (`npm run build` followed by `npm start`).
- [ ] The Eruda console functions correctly (logs, network, elements, etc.).

## Out of Scope
- Custom Eruda plugins or extensive styling.
- Persistence of Eruda settings across sessions (unless default).
