import pytest
from agent.tools.fundamentals import get_company_fundamentals, FundamentalsError

def test_fundamentals_returns_expected_keys():
    result = get_company_fundamentals("AAPL")
    expected_keys = {
        "ticker", "company_name", "sector", "industry", "market_cap",
        "pe_ratio", "forward_pe", "dividend_yield",
        "fifty_two_week_high", "fifty_two_week_low"
    }
    assert set(result.keys()) == expected_keys

def test_fundamentals_ticker_is_uppercase():
    result = get_company_fundamentals("aapl")
    assert result["ticker"] == "AAPL"

def test_fundamentals_market_cap_is_positive():
    result = get_company_fundamentals("AAPL")
    assert result["market_cap"] > 0

def test_fundamentals_raises_on_invalid_ticker():
    with pytest.raises(FundamentalsError):
        get_company_fundamentals("ZZZZZZZ")

def test_fundamentals_raises_on_empty_ticker():
    with pytest.raises(FundamentalsError):
        get_company_fundamentals("")