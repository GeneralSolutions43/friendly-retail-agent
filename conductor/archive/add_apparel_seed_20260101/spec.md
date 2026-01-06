# Spec: Add Athletic Apparel Seed Data

## Overview
Expand the product catalog by adding a medium set of athletic apparel to the database seed data. This will provide a broader base for product discovery and testing of the AI agent's semantic search capabilities.

## Functional Requirements
- **Data Expansion:** Add 10-15 new athletic apparel items to `backend/app/seed.py`.
- **Product Details:** Each new item must include:
    - Name (e.g., "Pro-Performance Leggings")
    - Category ("Apparel" or "Athletic Wear")
    - Price
    - Simple and direct description
    - Inventory count
- **Variety:** Include a mix of items such as leggings, shirts, shorts, and jackets designed for athletic activities.

## Technical Requirements
- Update the `seed_products` function in `backend/app/seed.py` to include the new data.
- Ensure the seeding process remains idempotent (avoids duplicates if run multiple times).

## Acceptance Criteria
- [ ] `backend/app/seed.py` contains the new athletic apparel items.
- [ ] The seeding script runs successfully without errors.
- [ ] New products are visible via the `/products` endpoint after re-seeding.
- [ ] The AI agent can successfully retrieve and discuss these new items.

## Out of Scope
- Adding real images for the new items.
- Modifying the database schema.
