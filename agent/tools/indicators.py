import pandas as pd
import numpy as np
from agent.tools.stock_price import get_stock_price

# Calculating annualized volatility based on daily log returns' standard deviation
def calculate_volatility(price_df: pd.DataFrame , window: int = 20) -> float:
    if price_df.empty or len(price_df) < window:
        raise ValueError("Insufficient data to calculate volatility.")
    
    closes = price_df['Close']
    log_returns = pd.Series( np.log(closes / closes.shift(1))).dropna()
    recent_returns = log_returns.tail(window)
    daily_std = recent_returns.std()
    annualized_volatility = daily_std * np.sqrt(252)
    return round(annualized_volatility, 4)

# Calulating Relative Strength Index
def calculate_rsi(price_df: pd.DataFrame , period: int = 14) -> float:
    if price_df.empty or len(price_df) < period:
        raise ValueError("Insufficient data to calculate RSI.")
    closes = price_df['Close']
    delta = closes.diff().dropna()
    gains = delta.where(delta > 0 , 0.0)
    losses = -delta.where(delta < 0 , 0.0)
    
    # Calculating the Avg Losses & Gains
    avg_gain = gains.rolling(window = period).mean().iloc[-1]
    avg_loss = losses.rolling(window = period).mean().iloc[-1]
    
    if avg_loss == 0:   
        return 100.0 # RSI is 100 if there are no losses
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return round(rsi , 2)

# Calculating Moving Average Convergence Divergence
def calculate_moving_averages(price_df : pd.DataFrame , short_window: int = 20 , long_window: int = 50) -> dict:
    if price_df.empty or len(price_df) < long_window:
        raise ValueError("Insufficient data to calculate moving averages.")
    closes = price_df['Close']
    sma_short = closes.rolling(window = short_window).mean().iloc[-1]
    sma_long = closes.rolling(window = long_window).mean().iloc[-1]
    
    ema_short = closes.ewm(span = short_window, adjust = False).mean().iloc[-1]
    ema_long = closes.ewm(span = long_window, adjust = False).mean().iloc[-1]
    
    return {
        "sma_short" : round(float(sma_short) , 2),
        "sma_long" : round(float(sma_long) , 2),
        "ema_short" : round(float(ema_short) , 2),
        "ema_long" : round(float(ema_long),2 ),
        "trend": "bullish" if sma_short > sma_long else "bearish"
    }
    
# Single entry point to get all indicators for a given stock symbol
def get_all_indicators(ticker: str , period: str = "3mo") -> dict:
    price_df = get_stock_price(ticker , period = period)
    volatility = calculate_volatility(price_df)
    rsi = calculate_rsi(price_df)
    moving_averages = calculate_moving_averages(price_df)
    return {
        "ticker" : ticker.strip().upper(),
        "volatility" : float(volatility),
        "rsi" : float(rsi),
        **moving_averages
    }