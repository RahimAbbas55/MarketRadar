import yfinance as yf

# fetches basic company fundamentals: market cap, P/E, sector, earnings dates
def get_company_fundamentals(ticker: str) -> dict:
    stock = yf.Ticker(ticker.strip().upper())
    info = stock.info

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