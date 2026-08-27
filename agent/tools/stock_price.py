import yfinance as yf
import pandas as pd

def get_stock_price(ticker: str , period: str = "1mo" , interval: str = "1d") -> pd.DataFrame:
    # Fetches OHLCV data for the provided interval/period
    stock = yf.Ticker(ticker)
    history = stock.history(period = period , interval = interval)
    return history