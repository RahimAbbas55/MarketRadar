import pytest
from agent.tools.compare import compare_assets

def test_compare_returns_entry_per_ticker():
    result = compare_assets(["TSLA", "RIVN"])
    assert set(result.keys()) == {"TSLA", "RIVN"}

def test_compare_successful_entries_have_status_ok():
    result = compare_assets(["TSLA", "RIVN"])
    assert result["TSLA"]["status"] == "ok"
    assert result["RIVN"]["status"] == "ok"

def test_compare_handles_invalid_ticker_gracefully():
    result = compare_assets(["TSLA", "ZZZZZZZ"])
    assert result["TSLA"]["status"] == "ok"
    assert result["ZZZZZZZ"]["status"] == "failed"
    assert "error" in result["ZZZZZZZ"]

def test_compare_raises_on_single_ticker():
    with pytest.raises(ValueError):
        compare_assets(["TSLA"])

def test_compare_raises_on_empty_list():
    with pytest.raises(ValueError):
        compare_assets([])