# Conductor Track Suggestions

This document tracks potential future features, improvements, and technical tasks for the Friendly Retail Agent project.

---

## 🧠 AI & Intelligence

### 1. AI Integration (The "Brain") - [COMPLETED]
*   **Description:** Replace mocked chat logic with a functional LLM (Llama 3 via Groq).
*   **Goal:** Enable dynamic, conversational responses instead of static mocks.

### 2. RAG Implementation (Product Knowledge) - [COMPLETED]
*   **Description:** Connect the LLM to the PostgreSQL database using Retrieval-Augmented Generation.
*   **Goal:** Enable the agent to answer specific questions about the inventory (e.g., "What are the cheapest shoes?").

### 3. AI Agent Memory (Conversation History) - [COMPLETED]
*   **Description:** Implement session management (likely via Redis) to store message history.
*   **Goal:** Support natural multi-turn conversations where the agent remembers context.

### 4. Streaming AI Responses - [COMPLETED]
*   **Description:** Update the backend and frontend to support real-time token streaming.
*   **Goal:** Improve the user experience by reducing perceived latency.

---

## 🛒 Storefront & UX

### 5. Store Demo Landing Page - [COMPLETED]
*   **Description:** Build a functional storefront landing page with product cards and a hero section.
*   **Goal:** Provide a realistic context for the floating chat overlay.

### 6. Enhanced Product Discovery
*   **Description:** Add UI filters (category, price) and a storefront search bar.
*   **Goal:** Improve manual navigation of the product catalog.

### 7. Semantic Search (Vector Search) - [COMPLETED]
*   **Description:** Implement vector embeddings for products to support "natural language" storefront search.
*   **Goal:** Help users find "winter gear" even if the product is named "Casual Hoodie".

---

## 👤 Personalization & Logic

### 8. User Profiles & History
*   **Description:** Add user accounts, login, and purchase history tracking.
*   **Goal:** Allow the AI to provide personalized recommendations based on past behavior.

### 9. Inventory & Order Tracking
*   **Description:** Add `Order` and `InventoryUpdate` tables and agent tools to query them.
*   **Goal:** Let users ask the agent "Where is my order?" or "Is this in stock at my local store?".

### 10. Automated Product Seeding
*   **Description:** Integrate with an external e-commerce API (like Shopify or a mock data generator) to keep the catalog fresh.
*   **Goal:** Scale the demo beyond the initial manual seed data.
