import pandas as pd
import numpy as np

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