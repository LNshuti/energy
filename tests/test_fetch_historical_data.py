import pytest
from src.main import fetch_historical_data

def test_fetch_historical_data_success(mock_yf_download, mock_yf_info, sample_data):
    ticker = 'AAPL'
    start_date = '2023-01-01'
    end_date = '2023-12-31'
    
    data, market_cap = fetch_historical_data(ticker, start_date, end_date)
    
    assert not data.empty
    assert market_cap == 150.0  # Since 150000000000 / 1e9 = 150

def test_fetch_historical_data_no_data(mock_yf_download, mock_yf_info):
    from unittest.mock import MagicMock
    mock_yf_download.return_value = MagicMock(empty=True)
    
    ticker = 'INVALID'
    start_date = '2023-01-01'
    end_date = '2023-12-31'
    
    data, market_cap = fetch_historical_data(ticker, start_date, end_date)
    
    assert data is None
    assert market_cap == 'N/A'

def test_fetch_historical_data_exception(mock_yf_download, mock_yf_info):
    mock_yf_download.side_effect = Exception("Network Error")

    ticker = 'AAPL'
    start_date = '2023-01-01'
    end_date = '2023-12-31'

    data, market_cap = fetch_historical_data(ticker, start_date, end_date)

    assert data is None
    assert market_cap is None