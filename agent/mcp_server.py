from mcp.server.fastmcp import FastMCP
from agent.tools.stock_price import get_stock_price, StockDataError
from agent.tools.indicators import get_all_indicators
from agent.tools.news import search_market_news, NewsSearchError
from agent.tools.fundamentals import get_company_fundamentals, FundamentalsError
from agent.tools.compare import compare_assets
from agent.tools.research import research_ticker

mcp = FastMCP("MarketRadar")
@mcp.tool()
def fetch_stock_price(ticker: str, period: str = "1mo", interval: str = "1d") -> dict:
    """Fetch historical OHLCV price data for a stock ticker."""
    try:
        df = get_stock_price(ticker, period=period, interval=interval)
        return df.tail(5).to_dict(orient="records")
    except StockDataError as e:
        return {"error": str(e)}

@mcp.tool()
def fetch_technical_indicators(ticker: str, period: str = "3mo") -> dict:
    """Get volatility, RSI, and moving averages for a stock ticker."""
    try:
        return get_all_indicators(ticker, period=period)
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def fetch_market_news(query: str) -> dict:
    """Search recent news articles related to a stock ticker or company name."""
    try:
        return {"articles": search_market_news(query)}
    except NewsSearchError as e:
        return {"error": str(e)}

@mcp.tool()
def fetch_company_fundamentals(ticker: str) -> dict:
    """Get company fundamentals: market cap, P/E ratio, sector, industry, 52-week range."""
    try:
        return get_company_fundamentals(ticker)
    except FundamentalsError as e:
        return {"error": str(e)}

@mcp.tool()
def compare_stocks(tickers: list[str]) -> dict:
    """Compare 2 or more stocks on volatility, RSI, trend, fundamentals, and recent news."""
    try:
        return compare_assets(tickers)
    except ValueError as e:
        return {"error": str(e)}

@mcp.tool()
def get_full_research(ticker: str) -> dict:
    """Get a complete research snapshot for a single stock: price indicators, fundamentals, and news."""
    try:
        return research_ticker(ticker)
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run(transport="stdio")