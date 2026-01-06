# Friendly Retail Agent - Frontend

This is the frontend for the Friendly Retail Agent, built with [Next.js](https://nextjs.org). It features a modern storefront demo and a persistent floating AI agent overlay.

## Features

- **Storefront Demo:** A responsive product catalog displaying items from the backend database.
- **Minimal AI Agent Overlay:** A fixed bottom-left chat interface with:
  - **Tone Selection:** Choose between "Helpful Professional", "Friendly Assistant", and "Expert Consultant".
  - **State Management:** Can be expanded, minimized, or dismissed.
- **Mobile Debugging:** Integrated [Eruda](https://github.com/liriliri/eruda) console available in development mode.

## Tech Stack

- **Framework:** Next.js 15+ (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Testing:** Jest & React Testing Library

## Getting Started

### Prerequisites

- Node.js 20+
- Backend service running (defaults to `http://localhost:8002`)

### Installation

```bash
cd frontend
npm install
```

### Development

Run the development server:

```bash
npm run dev
```

Open [http://localhost:3002](http://localhost:3002) with your browser to see the result.

### Testing

```bash
npm test
# With coverage
npm test -- --coverage
```

### Linting

```bash
npm run lint
```

## Environment Variables

The following environment variables can be configured:

- `NEXT_PUBLIC_API_URL`: The URL of the backend API (default: `http://localhost:8002`).