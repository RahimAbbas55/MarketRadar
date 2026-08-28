import yfinance as yf

class FundamentalsError(Exception):
    pass

# fetches basic company fundamentals: market cap, P/E, sector, earnings dates
def get_company_fundamentals(ticker: str) -> dict:
    
    # If no ticker provided
    if not ticker or not ticker.strip():
        raise FundamentalsError("Ticker symbol is required.")
    
    # Data sanitization
    ticker = ticker.strip().upper()
    stock = yf.Ticker(ticker)
    
    # Getting company info
    try:
        info = stock.info
    except Exception as e:
        raise FundamentalsError(f"Error fetching data for ticker '{ticker}': {str(e)}")

    # yfinance returns an empty dictionary if the ticker is invalid
    if not info or info.get("longName") is None:
        raise FundamentalsError(f"No fundamentals data found for ticker '{ticker}' — it may be invalid")

    return {
        "ticker": ticker.strip().upper(),
        "company_name": info.get("longName"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "forward_pe": info.get("forwardPE"),
        "dividend_yield": info.get("dividendYield"),
        "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
        "fifty_two_week_low": info.get("fiftyTwoWeekLow")
    }