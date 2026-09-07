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

### Terraform Stage 3 - Three isolated environments running from one codebase
![Cloud Run services showing prod, dev, and staging all deployed independently](assets/terraform-stage3/environments.png)

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