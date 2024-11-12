import pytest
import numpy as np
from unittest.mock import patch
from src.main import COMPANY_TICKERS

@pytest.fixture
def sample_data():
    """Sample dataframe resembling yfinance data."""
    import pandas as pd
    dates = pd.date_range(start="2023-01-01", periods=100, freq='D')
    data = pd.DataFrame({
        'Open': np.random.rand(100) * 100,
        'High': np.random.rand(100) * 100,
        'Low': np.random.rand(100) * 100,
        'Close': np.random.rand(100) * 100,
        'Volume': np.random.randint(1000000, 5000000, size=100)
    }, index=dates)
    return data

@pytest.fixture
def mock_yf_download(sample_data):
    with patch('src.main.yf.download') as mock_download:
        mock_download.return_value = sample_data
        yield mock_download

@pytest.fixture
def mock_yf_info():
    with patch('src.main.yf.Ticker') as mock_ticker:
        mock_instance = mock_ticker.return_value
        mock_instance.info = {'marketCap': 150000000000}  # Example market cap
        yield mock_ticker