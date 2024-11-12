import pytest
from src.main import select_all_indicators

def test_select_all_indicators_true():
    select_all = True
    indicators = select_all_indicators(select_all)
    expected = ["SMA", "MACD", "RSI", "Bollinger Bands"]
    assert indicators == expected

def test_select_all_indicators_false():
    select_all = False
    indicators = select_all_indicators(select_all)
    expected = []
    assert indicators == expected