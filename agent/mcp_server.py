from mcp.server.fastmcp import FastMCP
from agent.tools.stock_price import get_stock_price, StockDataError
from agent.tools.indicators import get_all_indicators
from agent.tools.news import search_market_news, NewsSearchError
from agent.tools.fundamentals import get_company_fundamentals, FundamentalsError
from agent.tools.compare import compare_assets
from agent.tools.research import research_ticker

mcp = FastMCP("MarketRadar")

# Fetch historical OHLCV price data for a stock ticker.
@mcp.tool()
def fetch_stock_price(ticker: str, period: str = "1mo", interval: str = "1d") -> dict:
    try:
        df = get_stock_price(ticker, period=period, interval=interval)
        return df.tail(5).to_dict(orient="records")
    except StockDataError as e:
        return {"error": str(e)}

# Get volatility, RSI, and moving averages for a stock ticker.
@mcp.tool()
def fetch_technical_indicators(ticker: str, period: str = "3mo") -> dict:
    try:
        return get_all_indicators(ticker, period=period)
    except Exception as e:
        return {"error": str(e)}

# Search recent news articles related to a stock ticker or company name.
@mcp.tool()
def fetch_market_news(query: str) -> dict:
    try:
        return {"articles": search_market_news(query)}
    except NewsSearchError as e:
        return {"error": str(e)}

# Get company fundamentals: market cap, P/E ratio, sector, industry, 52-week range.
@mcp.tool()
def fetch_company_fundamentals(ticker: str) -> dict:
    try:
        return get_company_fundamentals(ticker)
    except FundamentalsError as e:
        return {"error": str(e)}

# Compare 2 or more stocks on volatility, RSI, trend, fundamentals, and recent news.
@mcp.tool()
def compare_stocks(tickers: list[str]) -> dict:
    try:
        return compare_assets(tickers)
    except ValueError as e:
        return {"error": str(e)}

# Get a complete research snapshot for a single stock: price indicators, fundamentals, and news.
@mcp.tool()
def get_full_research(ticker: str) -> dict:
    try:
        return research_ticker(ticker)
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()