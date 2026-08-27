import yfinance as yf
import pandas as pd

class StockDataError(Exception):
    pass

# Fetches OHLCV data for the provided interval/period
def get_stock_price(ticker: str , period: str = "1mo" , interval: str = "1d") -> pd.DataFrame:
    # Check if ticker is provided
    if not ticker:
        raise StockDataError("Ticker symbol is required.")
        
    # Fetch the stock data using yfinance
    stock = yf.Ticker(ticker)
    history = stock.history(period = period , interval = interval)
    
    # If history is empty, raise an error
    if history.empty:
        raise StockDataError(f"No data found for ticker: {ticker} with period: {period} and interval: {interval}. It may be invalid")
    return history