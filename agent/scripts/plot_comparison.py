import matplotlib.pyplot as plt
from agent.tools.compare import compare_assets

# reuse the same tool you already built and tested
result = compare_assets(["TSLA", "RIVN"])

tickers = list(result.keys())
volatility = [result[t]["volatility"] for t in tickers]
rsi = [result[t]["rsi"] for t in tickers]

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.patch.set_facecolor("#0d0d0d")

colors = ["#00d4ff", "#ff6b6b"]

# volatility subplot
axes[0].bar(tickers, volatility, color=colors)
axes[0].set_title("Annualized Volatility", color="white", fontsize=13, pad=15)
axes[0].set_facecolor("#0d0d0d")
axes[0].tick_params(colors="white")
for spine in axes[0].spines.values():
    spine.set_color("#333333")

# RSI subplot
axes[1].bar(tickers, rsi, color=colors)
axes[1].axhline(70, color="#888888", linestyle="--", linewidth=1, label="Overbought (70)")
axes[1].axhline(30, color="#888888", linestyle="--", linewidth=1, label="Oversold (30)")
axes[1].set_title("RSI", color="white", fontsize=13, pad=15)
axes[1].set_facecolor("#0d0d0d")
axes[1].tick_params(colors="white")
axes[1].legend(
    facecolor="#1a1a1a", edgecolor="none", labelcolor="white", fontsize=8,
    loc="lower right", bbox_to_anchor=(1.0, 0.02)
)
axes[1].set_ylim(0, 85)  # headroom so legend doesn't collide with tall bars
for spine in axes[1].spines.values():
    spine.set_color("#333333")

fig.suptitle("MarketRadar — TSLA vs RIVN (Day 2)", color="white", fontsize=15)
plt.tight_layout()
plt.savefig("assets/day02/tsla_vs_rivn_comparison.png", dpi=200, facecolor="#0d0d0d")
plt.show()