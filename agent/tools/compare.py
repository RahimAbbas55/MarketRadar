from agent.tools.indicators import get_all_indicators
from agent.tools.fundamentals import get_company_fundamentals , FundamentalsError
from agent.tools.news import search_market_news, NewsSearchError
from agent.tools.stock_price import StockDataError

# Composite function: Pulls indicators, news, and tools for multiple ticker at a same time
def compare_assets(tickers: list[str]) -> dict:
    if not tickers or len(tickers) < 2:
        raise ValueError("compare_assets requires at least 2 tickers")
    
    comparison = {}
    
    # Iterate over each ticker and fetch data
    for ticker in tickers:
        # Sanitize the ticker input
        ticker = ticker.strip().upper()
        try: 
            # Fetch indicators, fundamentals, and news for the ticker
            indicators = get_all_indicators(ticker)
            fundamentals = get_company_fundamentals(ticker)
            news = search_market_news(ticker , page_size = 3)
            
            comparison[ticker] = {
                "status" : "ok",
                "volatility" : indicators.get("volatility"),
                "rsi" : indicators.get("rsi"),
                "trend" : indicators.get("trend"),
                "sector" : fundamentals.get("sector"),
                "market_cap" : fundamentals.get("market_cap"),
                "pe_ratio" : fundamentals.get("pe_ratio"),
                "recent_headlines": [article["title"] for article in news]
            }
        except (StockDataError , FundamentalsError , NewsSearchError) as e:
            comparison[ticker] = {
                "status": "failed",
                "error": str(e)
            }
    return comparison