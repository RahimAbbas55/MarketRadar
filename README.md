# MarketRadar

An MCP-powered agent for market and investment research. Ask natural-language questions like "compare Tesla and Rivian on volatility and recent news sentiment" and the agent chains together tool calls to pull live prices, compute technical indicators, search news, and synthesize an answer.

## Status
Day 1 complete — core data tools built and tested (price fetch + technical indicators).

## Tools (MCP) — Day 1 status
- `get_stock_price` — historical + current OHLCV data ✅ built + tested
- `calculate_technical_indicators` (volatility, RSI, moving averages) ✅ built + tested
- `search_market_news` — recent news by ticker/company ⏳ Day 2
- `get_company_fundamentals` — market cap, P/E, sector, earnings dates ⏳ Day 2
- `compare_assets` — composite multi-ticker comparison ⏳ Day 2

## Sample output

\`\`\`python
from agent.tools.indicators import get_all_indicators

result = get_all_indicators("TSLA")
print(result)

# {
#   'ticker': 'TSLA',
#   'volatility': 0.3726,
#   'rsi': 63.62,
#   'sma_short': 336.94,
#   'sma_long': 361.43,
#   'ema_short': 344.79,
#   'ema_long': 360.43,
#   'trend': 'bearish'
# }
\`\`\`

## Testing
\`\`\`
pytest agent/tests/ -v
\`\`\`

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