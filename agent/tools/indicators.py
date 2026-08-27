import pandas as pd
import numpy as np

# annualized volatility based on daily log returns' standard deviation
def calculate_volatility(price_df: pd.DataFrame , window: int = 20) -> float:
    if price_df.empty or len(price_df) < window:
        raise ValueError("Insufficient data to calculate volatility.")
    
    closes = price_df['Close']
    log_returns = pd.Series( np.log(closes / closes.shift(1))).dropna()
    recent_returns = log_returns.tail(window)
    daily_std = recent_returns.std()
    annualized_volatility = daily_std * np.sqrt(252)
    return round(annualized_volatility, 4)