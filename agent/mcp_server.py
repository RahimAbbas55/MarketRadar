from mcp.server.fastmcp import FastMCP
from agent.tools.stock_price import get_stock_price, StockDataError
from agent.tools.indicators import get_all_indicators

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

if __name__ == "__main__":
    mcp.run()