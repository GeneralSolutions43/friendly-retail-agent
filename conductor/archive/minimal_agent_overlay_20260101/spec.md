# Spec: Implement Minimal AI Agent Floating Overlay

## Overview
Implement a persistent floating AI agent interface positioned in the lower-left corner of the viewport. The design must strictly match the provided `@frontend/minimal_ai_agent_interface.html` (including animations, colors, and layout). The widget will be collapsible (minimized) and dismissible (hidden with a trigger to reopen).

## Functional Requirements
- **Positioning:** Fixed to the bottom-left of the viewport.
- **Visual Design:** Replicate the provided HTML/CSS styles exactly (RGB glow animation, dark theme, message styling).
- **State Management:**
    - **Open (Default):** Full interface visible (header, conversation, input).
    - **Minimized:** Only the header (or a summary bar) is visible.
    - **Dismissed:** Hides the main interface, leaving only a small trigger icon to reopen it.
- **Component Structure:** Implemented as a reusable React component (`MinimalAgentOverlay`).

## Interaction Requirements
- **Minimize Button:** A button in the header to toggle between Open and Minimized states.
- **Dismiss/Close Button:** A button to switch to the Dismissed state.
- **Trigger Icon:** When dismissed, a small floating icon (e.g., the logo) appears to reopen the agent.

## Out of Scope
- Backend integration for this specific visual update (we will use mock data or existing message logic if easy, but primary focus is UI).
- "Buy Me a Coffee" widget integration.
