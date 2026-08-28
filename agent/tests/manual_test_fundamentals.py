from agent.tools.fundamentals import get_company_fundamentals, FundamentalsError

TEST_TICKERS = ["AAPL", "TSLA", "RIVN", "NVDA"]

def run():
    for ticker in TEST_TICKERS:
        try:
            result = get_company_fundamentals(ticker)
            print(f"{ticker}: OK — {result['company_name']}, "
                  f"sector: {result['sector']}, "
                  f"market cap: {result['market_cap']:,}")
        except FundamentalsError as e:
            print(f"{ticker}: FAILED - {e}")

    # confirm error path still works inside this script
    try:
        get_company_fundamentals("ZZZZZZZ")
        print("ZZZZZZZ: unexpectedly succeeded — bug")
    except FundamentalsError as e:
        print(f"ZZZZZZZ: correctly caught - {e}")

if __name__ == "__main__":
    run()