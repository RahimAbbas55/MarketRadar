# MarketRadar

![Status](https://img.shields.io/badge/status-in--progress-yellow)
![Python](https://img.shields.io/badge/python-3.12-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991?logo=openai&logoColor=white)
![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-6E56CF)
![Terraform](https://img.shields.io/badge/Terraform-7B42BC?logo=terraform&logoColor=white)
![GCP](https://img.shields.io/badge/GCP-Cloud%20Run-4285F4?logo=googlecloud&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

An MCP-powered agent for market and investment research. Ask natural-language questions like "compare Tesla and Rivian on volatility and recent news sentiment" and the agent chains together tool calls to pull live prices, compute technical indicators, search news, and synthesize an answer.

## Status
MarketRadar is fully deployed and Terraform-managed, with infrastructure now modularized (Stage 2 of the Terraform roadmap complete) — frontend and backend both live on Google Cloud Run, with Artifact Registry and Secret Manager provisioned as infrastructure-as-code.

## Stack
- Python 3.12, OpenAI function calling, MCP SDK
- FastAPI backend, React + TypeScript frontend
- GCP (Cloud Run, Artifact Registry, Secret Manager) provisioned via modular Terraform

## Tools (MCP) — status
- `get_stock_price` — historical + current OHLCV data ✅ built + tested
- `calculate_technical_indicators` (volatility, RSI, moving averages) ✅ built + tested
- `search_market_news` — recent news by ticker/company ✅ built + tested
- `get_company_fundamentals` — market cap, P/E, sector, 52-week range ✅ built + tested
- `compare_assets` — multi-ticker comparison with partial-failure handling ✅ built + tested
- `research_ticker` — full single-ticker research snapshot ✅ built + tested
- MCP server wrapper (all 6 tools registered) ✅ built + tested
- Agent loop (OpenAI function calling + MCP execution) ✅ built + tested
- FastAPI layer with persistent MCP session ✅ built + tested
- Streaming chat endpoint (SSE, tool-call trace events) ✅ built + tested
- React frontend with live tool-call trace + markdown rendering ✅ built + tested
- Docker containerization (backend + frontend) ✅ built + tested
- GCP deployment via Terraform (Cloud Run, Artifact Registry, Secret Manager) ✅ live
- Terraform modularization (registry, secrets, compute modules) ✅ complete
- Multi-environment Terraform (dev/staging) ⏳ Stage 3
- Remote state + CI/CD ⏳ Stage 4
- Drift detection practice ⏳ Stage 5

## Daily Progress Log

### Day 1 — Core data tools
Built the foundational data-fetching layer.
- `get_stock_price` — historical + current OHLCV data via yfinance, with error handling for invalid tickers and empty responses
- `calculate_technical_indicators` — volatility (annualized, log-return based), RSI, and SMA/EMA moving averages
- `get_all_indicators` — composite function combining price fetch with all three indicators in one call
- Manual test scripts + unit tests (pytest) covering both happy paths and error cases
- Debugging note: chased a false bug caused by a stale Python shell session not picking up file edits — reinforced the habit of restarting the interpreter after every code change

### Day 2 — News, fundamentals, and comparison
Rounded out the data layer and built the first composite research tools.
- `search_market_news` — recent news search via NewsAPI, with rate-limit and network error handling
- `get_company_fundamentals` — market cap, P/E ratios, sector, industry, 52-week range via yfinance
- `compare_assets` — multi-ticker comparison tool with partial-failure handling, so one invalid ticker doesn't crash the whole request
- `research_ticker` — master function returning a full research snapshot (price, indicators, fundamentals, news) for a single ticker
- Full unit test coverage for fundamentals and comparison logic
- Known limitation surfaced: NewsAPI's keyword search can return loosely related results (e.g. "Apple" matching unrelated articles) — flagged for the agent layer to handle during synthesis
- Debugging note: a "fixed" bug wasn't actually fixed because the file had been edited but the Python session was stale — same root cause as Day 1, now a known gotcha

### Day 3 — MCP server + agent loop
The biggest day yet: wrapped all tools as an MCP server, then built and verified the actual AI agent on top of it.

**MCP server**
- Scaffolded with FastMCP, pinned to `mcp<2` after discovering the installed 2.x version renamed `FastMCP` to `MCPServer` with a different API
- Registered all 6 tools using `@mcp.tool()` decorators
- Built a real MCP client test that spawns the server as a subprocess and communicates over stdio, exactly how an AI agent would connect to it

**Agent loop**
- Built the core loop: OpenAI (gpt-4o) receives the user's question and available tools, decides which to call, we execute them via the live MCP session, and feed results back until the model has enough to answer
- Converted MCP tool schemas directly into OpenAI's function-calling format, reusing the JSON Schema FastMCP already generates from type hints
- Verified single-tool questions ("what's Tesla's RSI") and multi-tool chaining questions ("compare Tesla and Rivian, which is riskier") — the second correctly triggered 3 tool calls and produced a real reasoned judgment based on both volatility numbers and news sentiment, not just a data dump
- Added error handling so a failed tool call doesn't crash the loop — the model receives the error as if it were a normal tool response and explains it naturally to the user
- Added a max iteration safety limit to prevent infinite tool-calling loops

**Debugging notes**
- Tool descriptions were blank because they were written as `#` comments above each function instead of actual docstrings inside the function body — MCP reads `__doc__`, not source comments
- The server file had no `if __name__ == "__main__": mcp.run()` block at all, so it exited immediately instead of listening for connections — surfaced as a confusing "Connection closed" error on the client side with no other clues
- Multi-line async code doesn't paste cleanly into the interactive Python REPL due to indentation parsing — worth just using script files for anything beyond a one-liner

### Day 4 — FastAPI, streaming, and full frontend
The biggest single day yet — went from a backend-only agent to a complete, usable product.

**Backend**
- Built a FastAPI app with a persistent MCP session managed via lifespan context, avoiding a new subprocess per request
- Added both `POST /chat` (standard) and `POST /chat/stream` (SSE) endpoints
- Fixed a CORS issue where the browser's automatic preflight `OPTIONS` request was being rejected with 405, since FastAPI had no CORS middleware configured

**Frontend**
- Scaffolded with React + Vite + TypeScript
- Built a chat UI wired to the streaming endpoint via manual SSE parsing (browsers' built-in `EventSource` doesn't support POST, so the protocol is parsed by hand from a `fetch` response stream)
- Added a live tool-call trace so the user sees "Calling compare stocks..." in real time while the agent works, not just a loading spinner
- Added markdown rendering for assistant responses, since the LLM naturally formats answers with headers and bullet points that were previously showing as raw `###` and `**` characters
- Full dark theme redesign matching the project's purple brand identity
- Polish: auto-scroll to latest message, visually distinct error states for connection failures, auto-focus back to the input after each response

**Debugging notes**
- CORS preflight requests fail silently as generic 405s with no indication of the real cause unless you know to look for missing `CORSMiddleware`
- SSE responses can arrive split mid-event across network chunk boundaries — buffering and re-joining partial lines is required, not optional, for reliable parsing

### Day 5 — Containerization and live deployment
MarketRadar went from "runs on my machine" to actually live on the internet.

- Wrote a Dockerfile for the backend (Python 3.12, FastAPI + MCP subprocess in one container) and verified it locally before touching the cloud
- Wrote a multi-stage Dockerfile for the frontend (Node build stage → nginx serving stage), keeping the final image lean by discarding the Node.js toolchain entirely from the shipped image
- Set up a new GCP project, enabled Cloud Run, Artifact Registry, Secret Manager, and Cloud Build
- Pushed both images to Artifact Registry and deployed both services to Cloud Run
- Configured the frontend to use a build-time environment variable (`VITE_API_URL`) for the backend URL, so local development and production point to different backends without code changes
- Updated backend CORS to allow the deployed frontend's origin

**Debugging notes**
- Hit a GCP project quota limit while creating a new project — discovered that deleted projects still count against quota for a 30-day grace period, meaning deleting old projects doesn't free up quota immediately. Switched to a different Google account to unblock progress.
- Backend deployment failed with a cryptic `exec format error` and no further explanation from `gcloud`. Root cause: Docker images built on Apple Silicon default to `arm64`, but Cloud Run requires `amd64`. Fixed by explicitly building with `--platform linux/amd64`.
- CORS needed updating twice: once for local container-to-container testing (new localhost port), once for the actual deployed frontend origin — a reminder that CORS configuration needs revisiting at every new environment, not just once.

Both services verified end-to-end in production: a real question, through the live frontend, hits the live backend, spins up the MCP subprocess, calls OpenAI, and returns a grounded answer — the full pipeline working exactly as it does locally, just now reachable from anywhere.

### Terraform Stage 1 — From manual deployment to infrastructure-as-code
Took the manually deployed GCP infrastructure and brought it fully under Terraform management.

- Set up the Google provider and defined the Artifact Registry repository, both Cloud Run services (frontend + backend), and Secret Manager resources for API keys entirely in `.tf` files
- Moved API keys out of plain Cloud Run environment variables into Secret Manager, with proper IAM bindings granting Cloud Run's service account read access
- Used `terraform import` to bring the already-existing, manually-created resources (Artifact Registry repo, both Cloud Run services) under Terraform's management without destroying and recreating them — verified via `terraform plan` showing zero unwanted destroys before ever running apply
- Ran a clean `terraform apply` twice (once for the backend + secrets, once for the frontend), both completing without errors

**Debugging notes**
- Accidentally committed a 109MB Terraform provider binary before `.gitignore` caught up, which GitHub rejected outright. Fixed by resetting local commits (safe since they hadn't been pushed yet) and redoing them with `.terraform/` properly excluded from the start.
- `terraform plan` briefly displayed both real API keys in plaintext during a diff, since existing (non-sensitive-declared) resource values aren't masked the same way `sensitive` variables are. Rotated both keys immediately as a precaution.
- Discovered intermittent yfinance failures specifically in the deployed (Cloud Run) environment — Yahoo Finance occasionally rate-limits or briefly rejects requests from cloud provider IP ranges, since yfinance is an unofficial library, not a stable public API. The existing error handling already handles this gracefully; retrying the same request shortly after typically succeeds.
- Learned that using `:latest` as an image tag in Terraform means Terraform can't detect when the underlying image changes, since the tag string never changes — a real limitation worth addressing with versioned tags or digests in a future pass.

MarketRadar's entire GCP footprint — registry, both services, secrets, and IAM — can now be destroyed and recreated from scratch with `terraform apply`, with zero manual `gcloud` commands required.

### Terraform Stage 2 — Modularization
Refactored the flat `main.tf` into three reusable modules: `registry` (Artifact Registry), `secrets` (Secret Manager secret + version + IAM access, bundled as one unit), and `compute` (Cloud Run service + public IAM binding, parameterized to handle both plain env vars and Secret Manager-sourced ones via a `dynamic` block).

- The `compute` module is called twice (backend, frontend) and the `secrets` module is called twice (OpenAI key, NewsAPI key) — replacing what were previously near-duplicate resource blocks with single, reusable definitions
- Used `terraform state mv` to remap all 11 existing resources from their old flat addresses to their new module-based addresses, without touching any real infrastructure — verified via `terraform plan` showing 0 to add and 0 to destroy both before and after the move
- The only actual change applied was a harmless metadata normalization on the frontend service (clearing `client`/`client_version` fields originally set by `gcloud`, since the resource is now fully Terraform-managed)

**Debugging note:** A `git push` was rejected by GitHub's secret scanning push protection after Terraform's automatic timestamped state backup files (`terraform.tfstate.<timestamp>.backup`, created during each `state mv` operation) were accidentally committed, exposing API keys in plaintext. `.gitignore` only had `terraform.tfstate.backup` covered, not the timestamped variant Terraform actually generates. Fixed by broadening the ignore pattern and resetting the unpushed commit before recommitting cleanly. Both API keys were rotated as a precaution.

This is the safe way to refactor Terraform code for infrastructure that's already live — the alternative (not using `state mv`) would have destroyed and recreated the entire running application.

## Deployment

**Frontend (live):** https://marketradar-frontend-533485774082.us-central1.run.app/
**Backend (live):** https://marketradar-backend-533485774082.us-central1.run.app

Both services provisioned entirely via modular Terraform (see `terraform/`), containerized with Docker, pushed via Artifact Registry.

### Known limitation: intermittent yfinance failures in cloud environments
Since yfinance is an unofficial library accessing Yahoo Finance's internal endpoints (not a stable public API), requests from cloud provider IP ranges (including GCP) are occasionally rate-limited or briefly rejected. This surfaces as an "insufficient data" error on some requests, which the agent explains gracefully rather than crashing, but the same question retried shortly after often succeeds. This is a known constraint of the underlying data source, not a bug in the application logic.

### Note on Apple Silicon builds
Docker images built on an Apple Silicon Mac (M1/M2/M3) default to `arm64` architecture, but Cloud Run requires `amd64`. Build with the platform flag explicitly:

docker build --platform linux/amd64 -t <image-name> .

Omitting this causes a cryptic `exec format error` on Cloud Run with no indication of the real cause — the container image builds and pushes successfully, and only fails at the Cloud Run startup health check stage.

## Progress Gallery

### Day 1 — Price data + technical indicators
![TSLA price with moving averages](assets/day01/tsla_day1_chart.png)

### Day 2 — Multi-ticker comparison
![TSLA vs RIVN volatility and RSI comparison](assets/day02/tsla_vs_rivn_comparison.png)

### Day 3 - MCP server + agent loop
![TSLA vs RIVN volatility and RSI comparison](assets/day03/Day_3.png)

### Day 4 - Chat UI Working
![Chat UI Working](assets/day04/Day_04.png)

### Day 5 - Live on Google Cloud Run
![MarketRadar front-end deployed and running on Cloud Run](assets/day05/mr-fn.png)

![MarketRadar back-end deployed and running on Cloud Run](assets/day05/mr-b.png)

## Sample output — research_ticker

```python
from agent.tools.research import research_ticker

result = research_ticker("NVDA")

# {
#   "ticker": "NVDA",
#   "company_name": "NVIDIA Corporation",
#   "sector": "Technology",
#   "market_cap": 5253179637760,
#   "pe_ratio": 27.5,
#   "forward_pe": 14.2,
#   "volatility": 0.4627,
#   "rsi": 50.0,
#   "trend": "bullish",
#   "recent_headlines": [...]
# }
```

## Setup

pip install -r requirements.txt
cp .env.example .env # add your API keys

## Testing

pytest agent/tests/ -v


## Known limitations
- News search uses loose keyword matching (NewsAPI), which can occasionally surface tangentially related articles (e.g. searching "Apple" returning unrelated results). The agent layer will need to account for this when synthesizing answers.