from agent.tools.stock_price import get_stock_price, StockDataError
TEST_TICKERS = ["AAPL", "TSLA", "RIVN", "NVDA"]

def run():
    for ticker in TEST_TICKERS:
        try:
            df = get_stock_price(ticker)
            print(f"{ticker} - OK.\n{len(df)} rows, latest close = {df['Close'].iloc[-1]:.2f}")
        except StockDataError as e:
            print(f"{ticker}: FAILED - {e}")
        
        # Ensuring that error works here as well
    try:
        get_stock_price("ZZZZZZ")
        print("ZZZZZZZ: unexpectedly succeeded — bug")
    except StockDataError as e:
          print(f"ZZZZZZZ: correctly caught - {e}")
          
if __name__ == "__main__":
    run()