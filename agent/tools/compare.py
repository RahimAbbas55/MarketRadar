from agent.tools.indicators import get_all_indicators
from agent.tools.fundamentals import get_company_fundamentals
from agent.tools.news import search_market_news

# Composite function: Pulls indicators, news, and tools for multiple ticker at a same time
def compare_assets(tickers: list[str]) -> dict:
    comparison = {}
    
    # Iterate over each ticker and fetch data
    for ticker in tickers:
        # Sanitize the ticker input
        ticker = ticker.strip().upper()
        
        # Fetch indicators, fundamentals, and news for the ticker
        indicators = get_all_indicators(ticker)
        fundamentals = get_company_fundamentals(ticker)
        news = search_market_news(ticker)
        
        comparison[ticker] = {
            "volatility" : indicators.get("volatility"),
            "rsi" : indicators.get("rsi"),
            "trend" : indicators.get("trend"),
            "sector" : fundamentals.get("sector"),
            "market_cap" : fundamentals.get("market_cap"),
            "pe_ratio" : fundamentals.get("pe_ratio"),
            "recent_headlines": [article["title"] for article in news]
        }
    return comparison