import pytest
from src.main import fetch_and_plot, select_all_indicators
from unittest.mock import patch

def test_fetch_and_plot_single_company_single_indicator(mock_yf_download, mock_yf_info, sample_data):
    company_names = ['Enterprise Products Partners']
    indicator_types = ['SMA']
    
    images, error_message, total_market_cap = fetch_and_plot(company_names, indicator_types)
    
    assert len(images) == 1
    assert error_message == ""
    assert total_market_cap == "Total Market Cap: $150.00 Billion"

def test_fetch_and_plot_multiple_companies_single_indicator(mock_yf_download, mock_yf_info, sample_data):
    company_names = ['Enterprise Products Partners', 'Kinder Morgan']
    indicator_types = ['MACD']
    
    images, error_message, total_market_cap = fetch_and_plot(company_names, indicator_types)
    
    assert len(images) == 2
    assert error_message == ""
    assert total_market_cap == "Total Market Cap: $300.00 Billion"

def test_fetch_and_plot_exceed_company_limit():
    company_names = list(COMPANY_TICKERS.keys())[:8]
    indicator_types = ['SMA']
    
    images, error_message, total_market_cap = fetch_and_plot(company_names, indicator_types)
    
    assert images is None
    assert error_message == "You can select up to 7 companies at the same time."
    assert total_market_cap is None

def test_fetch_and_plot_multiple_indicators_multiple_companies():
    company_names = ['Enterprise Products Partners', 'Kinder Morgan']
    indicator_types = ['SMA', 'MACD']
    
    images, error_message, total_market_cap = fetch_and_plot(company_names, indicator_types)
    
    assert images is None
    assert error_message == "You can only select one indicator when selecting multiple companies."
    assert total_market_cap is None