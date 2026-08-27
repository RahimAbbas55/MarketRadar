import matplotlib.pyplot as plt
from agent.tools.stock_price import get_stock_price

# fetch the same data you already used today
df = get_stock_price("TSLA", period="3mo")
closes = df["Close"]

# recreate the same short/long windows used in calculate_moving_averages
sma_short = closes.rolling(window=20).mean()
sma_long = closes.rolling(window=50).mean()

plt.figure(figsize=(10, 6))
plt.plot(df.index, closes, label="TSLA Close", color="#e0e0e0", linewidth=1.5)
plt.plot(df.index, sma_short, label="20-day SMA", color="#00d4ff", linewidth=2)
plt.plot(df.index, sma_long, label="50-day SMA", color="#ff6b6b", linewidth=2)

plt.title("TSLA Price with Moving Averages — MarketRadar Day 1", fontsize=14, color="white")
plt.xlabel("Date", color="white")
plt.ylabel("Price (USD)", color="white")
plt.legend(facecolor="#1a1a1a", edgecolor="none", labelcolor="white")
plt.gca().set_facecolor("#0d0d0d")
plt.gcf().set_facecolor("#0d0d0d")
plt.tick_params(colors="white")
plt.grid(color="#333333", linewidth=0.5)

plt.tight_layout()
plt.savefig("tsla_day1_chart.png", dpi=200, facecolor="#0d0d0d")
plt.show()