import pytest
from src.main import fetch_historical_data
from unittest.mock import patch, MagicMock


@patch('src.main.yf.Ticker')
@patch('src.main.yf.download')
def test_fetch_historical_data_exception(mock_yf_download, mock_yf_Ticker):
    # Mock the yf.download function to raise an exception
    mock_yf_download.side_effect = Exception("Network Error")
    
    # Mock the yf.Ticker to avoid any side effects
    mock_yf_Ticker.return_value = MagicMock()
    
    ticker = 'AAPL'
    start_date = '2023-01-01'
    end_date = '2023-12-31'
    
    data, market_cap = fetch_historical_data(ticker, start_date, end_date)
    
    assert data is None
    assert market_cap is None  

@patch('src.main.yf.Ticker')
@patch('src.main.yf.download')
def test_fetch_historical_data_no_data(mock_yf_download, mock_yf_info):
    from unittest.mock import MagicMock
    mock_yf_download.return_value = MagicMock(empty=True)
    
    ticker = 'INVALID'
    start_date = '2023-01-01'
    end_date = '2023-12-31'
    
    data, market_cap = fetch_historical_data(ticker, start_date, end_date)
    
    assert data is None
    assert market_cap == 'N/A'

