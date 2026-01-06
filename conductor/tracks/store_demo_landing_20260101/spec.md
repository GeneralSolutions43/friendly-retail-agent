# Spec: Store Demo Landing Page

## Overview
Transform the minimalist Home page into a functional storefront demo. This will provide a realistic environment for the floating AI agent overlay, allowing users to browse products that the agent can later discuss.

## Functional Requirements
- **Hero Section:** A visually appealing top section welcoming users to the "Friendly Retail Store".
- **Product Grid:** A responsive grid layout displaying product cards.
- **Product Cards:** Each card must display:
    - Product Name
    - Category
    - Price
    - A short description snippet
    - A placeholder image
- **Data Fetching:** Products will be fetched on the server (Next.js Server Components) to demonstrate modern patterns.

## Technical Requirements
- **Backend Endpoint:** Ensure there is a generic `/products` endpoint or use `/products/search` with an empty/default query to fetch all items.
- **Styling:** Use Tailwind CSS to create a modern, high-contrast UI that matches the minimalist aesthetic of the project.

## Acceptance Criteria
- [ ] Home page displays a Hero section and a list of at least 5 products (from the seeded database).
- [ ] Product cards are responsive (stack on mobile, grid on desktop).
- [ ] The `MinimalAgentOverlay` remains accessible and functional on top of the storefront.
- [ ] No regressions in build or test status.

## Out of Scope
- Detailed "Product View" pages (clicking a card does nothing for now).
- "Add to Cart" or Checkout functionality.
- Real images (placeholders only).
