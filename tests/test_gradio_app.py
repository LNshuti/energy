# tests/test_gradio_app.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from src.main import fetch_and_plot, select_all_indicators, COMPANY_TICKERS

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'Open': [100] * 100,
        'High': [110] * 100,
        'Low': [90] * 100,
        'Close': [105] * 100,
        'Volume': [1000000] * 100
    })

@pytest.fixture
def mock_yf_download(monkeypatch, sample_data):
    mock = MagicMock(return_value=sample_data)
    monkeypatch.setattr('yfinance.download', mock)
    return mock

@pytest.fixture
def mock_yf_info(monkeypatch):
    mock = MagicMock()
    mock.info = {'marketCap': 150000000000}  # $150B market cap
    monkeypatch.setattr('yfinance.Ticker', lambda *args: mock)
    return mock

@patch('src.main.yf.Ticker')
@patch('src.main.yf.download')
def test_fetch_and_plot_single_company_single_indicator(mock_yf_download, mock_yf_info, sample_data):
    mock_yf_download.return_value = sample_data
    mock_yf_info.return_value.info = {'marketCap': 150000000000}
    
    company_names = ['Enterprise Products Partners']
    indicator_types = ['SMA']
    
    images, error_message, total_market_cap = fetch_and_plot(company_names, indicator_types)
    
    assert isinstance(images, list)
    assert len(images) == 1
    assert error_message is None
    assert isinstance(total_market_cap, float)
    assert total_market_cap == 150.0

@patch('src.main.yf.Ticker')
@patch('src.main.yf.download')
def test_fetch_and_plot_multiple_companies_single_indicator(mock_yf_download, mock_yf_info, sample_data):
    # Setup mocks
    mock_yf_download.return_value = sample_data
    mock_ticker = MagicMock()
    mock_ticker.info = {'marketCap': 150000000000}
    mock_yf_info.return_value = mock_ticker
    
    company_names = ['Enterprise Products Partners', 'Kinder Morgan']
    indicator_types = ['MACD']
    
    # Call function
    images, error_message, total_market_cap = fetch_and_plot(company_names, indicator_types)
    
    # Verify results
    assert isinstance(images, list)
    assert len(images) == 2
    assert error_message is None
    assert isinstance(total_market_cap, float)
    assert total_market_cap == 300.0

@patch('src.main.yf.Ticker')
@patch('src.main.yf.download')
def test_fetch_and_plot_exceed_company_limit(mock_yf_download, mock_yf_info):
    company_names = list(COMPANY_TICKERS.keys())[:8]
    indicator_types = ['SMA']
    
    images, error_message, total_market_cap = fetch_and_plot(company_names, indicator_types)
    
    assert images is None
    assert error_message == "Exceeded company limit"
    assert total_market_cap is None

@patch('src.main.yf.Ticker')
@patch('src.main.yf.download')
def test_fetch_and_plot_multiple_indicators_multiple_companies(mock_yf_download, mock_yf_info):
    company_names = ['Enterprise Products Partners', 'Kinder Morgan']
    indicator_types = ['SMA', 'MACD']

    images, error_message, total_market_cap = fetch_and_plot(company_names, indicator_types)
    
    assert images is None
    assert error_message == "Multiple indicators not supported"
    assert total_market_cap is None