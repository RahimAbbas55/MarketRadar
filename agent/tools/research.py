from agent.tools.indicators import get_all_indicators
from agent.tools.fundamentals import get_company_fundamentals
from agent.tools.news import search_market_news

# single entry point: full research snapshot for one ticker
def research_ticker(ticker: str) -> dict:
    ticker = ticker.strip().upper()

    indicators = get_all_indicators(ticker)
    fundamentals = get_company_fundamentals(ticker)
    news = search_market_news(ticker, page_size=5)

    return {
        "ticker": ticker,
        "company_name": fundamentals["company_name"],
        "sector": fundamentals["sector"],
        "industry": fundamentals["industry"],
        "market_cap": fundamentals["market_cap"],
        "pe_ratio": fundamentals["pe_ratio"],
        "forward_pe": fundamentals["forward_pe"],
        "fifty_two_week_high": fundamentals["fifty_two_week_high"],
        "fifty_two_week_low": fundamentals["fifty_two_week_low"],
        "volatility": indicators["volatility"],
        "rsi": indicators["rsi"],
        "trend": indicators["trend"],
        "sma_short": indicators["sma_short"],
        "sma_long": indicators["sma_long"],
        "recent_headlines": [article["title"] for article in news]
    }