# MarketRadar — Frontend

React + TypeScript chat interface for MarketRadar, an AI agent for market and investment research. Talks to the FastAPI backend's streaming endpoint and renders the agent's tool-call trace live as it works.

## Features

- Real-time streaming chat via Server-Sent Events (SSE), parsed manually from a `fetch` response stream (browsers' built-in `EventSource` doesn't support POST requests, which this API requires)
- Live tool-call trace — shows which tool the agent is calling (e.g. "Calling Compare stocks...") while it works, not just a loading spinner
- Markdown rendering for assistant responses (headers, bold text, bullet lists)
- Distinct visual state for connection errors vs normal responses
- Auto-scroll to the latest message, auto-focus back to the input after each response

## Stack

- React 18 + TypeScript
- Vite (dev server + build tool)
- `react-markdown` for rendering formatted agent responses

## Setup

```bash
npm install
npm run dev
```

Runs on `http://localhost:5173` by default.

## Requirements

The backend must be running for this to work — see the root `README.md` for backend setup. By default, the frontend expects the API at `http://localhost:8000` (set in `src/App.tsx` via `API_URL`).

## Build

```bash
npm run build
```

Outputs a production build to `dist/`.

## Project structure

```
src/
├── App.tsx       # main chat component: state, SSE streaming logic, UI
├── App.css       # dark theme styling matching the project's purple brand
└── main.tsx      # React entry point
```