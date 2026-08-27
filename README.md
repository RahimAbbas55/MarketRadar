# MarketRadar

An MCP-powered agent for market and investment research. Ask natural-language questions like "compare Tesla and Rivian on volatility and recent news sentiment" and the agent chains together tool calls to pull live prices, compute technical indicators, search news, and synthesize an answer.

## Status
Early build — Day 1: core data tools (price fetch, technical indicators).

## Stack
- Python 3.12, OpenAI function calling, MCP SDK
- FastAPI backend, React + TypeScript frontend
- GCP (Cloud Run, Artifact Registry, Secret Manager) provisioned via Terraform

## Tools (MCP)
- `get_stock_price` — historical + current OHLCV data
- `calculate_technical_indicators` — volatility, RSI, moving averages
- `search_market_news` — recent news by ticker/company
- `get_company_fundamentals` — market cap, P/E, sector, earnings dates
- `compare_assets` — composite multi-ticker comparison

## Setup
\`\`\`
pip install -r requirements.txt
cp .env.example .env  # add your API keys
\`\`\`