import pytest
from src.main import plot_indicators

def test_plot_indicators_single_company_single_indicator(mock_yf_download, mock_yf_info, sample_data):
    company_names = ['Enterprise Products Partners']
    indicator_types = ['SMA']
    
    images, error_message, total_market_cap = plot_indicators(company_names, indicator_types)
    
    assert len(images) == 1
    assert error_message == ""
    assert total_market_cap == 150.0

def test_plot_indicators_multiple_companies_single_indicator(mock_yf_download, mock_yf_info, sample_data):
    company_names = ['Enterprise Products Partners', 'Kinder Morgan']
    indicator_types = ['MACD']
    
    images, error_message, total_market_cap = plot_indicators(company_names, indicator_types)
    
    assert len(images) == 2
    assert error_message == ""
    assert total_market_cap == 300.0  # 150 + 150

def test_plot_indicators_exceed_company_limit(mock_yf_download, mock_yf_info, sample_data):
    company_names = list(COMPANY_TICKERS.keys())[:8]  # 8 companies
    indicator_types = ['SMA']
    
    images, error_message, total_market_cap = plot_indicators(company_names, indicator_types)
    
    assert images is None
    assert error_message == "You can select up to 7 companies at the same time."
    assert total_market_cap is None

def test_plot_indicators_multiple_indicators_multiple_companies(mock_yf_download, mock_yf_info, sample_data):
    company_names = ['Enterprise Products Partners', 'Kinder Morgan']
    indicator_types = ['SMA', 'MACD']
    
    images, error_message, total_market_cap = plot_indicators(company_names, indicator_types)
    
    assert images is None
    assert error_message == "You can only select one indicator when selecting multiple companies."
    assert total_market_cap is None

def test_plot_indicators_with_no_data(mock_yf_download, mock_yf_info, sample_data):
    from unittest.mock import MagicMock
    mock_yf_download.return_value = MagicMock(empty=True)
    
    company_names = ['Enterprise Products Partners']
    indicator_types = ['SMA']
    
    images, error_message, total_market_cap = plot_indicators(company_names, indicator_types)
    
    assert len(images) == 0
    assert error_message == ""
    assert total_market_cap == 0