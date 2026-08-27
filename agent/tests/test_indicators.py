import pytest
from agent.tools.stock_price import get_stock_price
from agent.tools.indicators import calculate_volatility, calculate_rsi, calculate_moving_averages

@pytest.fixture(scope="module")
def tsla_data():
    # fetched once and reused across tests in this file to avoid hammering the API
    return get_stock_price("TSLA", period="3mo")

def test_volatility_returns_positive_float(tsla_data):
    vol = calculate_volatility(tsla_data)
    assert isinstance(vol, float)
    assert vol > 0

def test_rsi_within_valid_range(tsla_data):
    rsi = calculate_rsi(tsla_data)
    assert 0 <= rsi <= 100

def test_moving_averages_returns_expected_keys(tsla_data):
    mas = calculate_moving_averages(tsla_data)
    expected_keys = {"sma_short", "sma_long", "ema_short", "ema_long", "trend"}
    assert set(mas.keys()) == expected_keys
    assert mas["trend"] in ("bullish", "bearish")

def test_moving_averages_values_are_plain_floats(tsla_data):
    mas = calculate_moving_averages(tsla_data)
    assert isinstance(mas["sma_short"], float)
    assert isinstance(mas["ema_long"], float)

def test_volatility_raises_on_insufficient_data():
    import pandas as pd
    empty_df = pd.DataFrame({"Close": [100.0]})
    with pytest.raises(ValueError):
        calculate_volatility(empty_df)