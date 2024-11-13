# tests/test_gradio_app.py

import sys
import os
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.main import fetch_and_plot, COMPANY_TICKERS

# Set Matplotlib backend to 'Agg' to prevent plotting issues in headless environments
import matplotlib
matplotlib.use('Agg')


@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'Open': [100] * 100,
        'High': [110] * 100,
        'Low': [90] * 100,
        'Close': [105] * 100,
        'Volume': [1000000] * 100
    })


@patch('src.main.plot_indicator')  # Mock plot_indicator first
@patch('src.main.yf.Ticker')
@patch('src.main.yf.download')
def test_fetch_and_plot_single_company_single_indicator(mock_download, mock_info, mock_plot_indicator, sample_data):
    # Setup mocks
    mock_download.return_value = sample_data

    # Mock Ticker.info to return a market cap of 150,000,000,000
    mock_ticker = MagicMock()
    mock_ticker.info = {'marketCap': 150000000000}
    mock_info.return_value = mock_ticker

    # Mock plot_indicator to return a mock image
    mock_plot_indicator.return_value = MagicMock()

    company_names = ['Enterprise Products Partners']
    indicator_types = ['SMA']

    # Call the function
    images, error_message, total_market_cap = fetch_and_plot(company_names, indicator_types)

    # Verify results
    assert isinstance(images, list), "Images should be a list."
    assert len(images) == 1, f"Expected 1 image, got {len(images)}."
    assert error_message is None, f"Expected no error message, got '{error_message}'."
    assert isinstance(total_market_cap, float), "Total market cap should be a float."
    assert total_market_cap == 150.0, f"Expected total market cap of 150.0, got {total_market_cap}."


@patch('src.main.plot_indicator')  # Mock plot_indicator first
@patch('src.main.yf.Ticker')
@patch('src.main.yf.download')
def test_fetch_and_plot_multiple_companies_single_indicator(mock_download, mock_info, mock_plot_indicator, sample_data):
    # Setup mocks
    mock_download.return_value = sample_data

    # Mock Ticker.info to return a market cap of 150,000,000,000 for each company
    mock_ticker = MagicMock()
    mock_ticker.info = {'marketCap': 150000000000}
    mock_info.return_value = mock_ticker

    # Mock plot_indicator to return a mock image
    mock_plot_indicator.return_value = MagicMock()

    company_names = ['Enterprise Products Partners', 'Kinder Morgan']
    indicator_types = ['MACD']

    # Call the function
    images, error_message, total_market_cap = fetch_and_plot(company_names, indicator_types)

    # Verify results
    assert isinstance(images, list), "Images should be a list."
    assert len(images) == 2, f"Expected 2 images, got {len(images)}."
    assert error_message is None, f"Expected no error message, got '{error_message}'."
    assert isinstance(total_market_cap, float), "Total market cap should be a float."
    assert total_market_cap == 300.0, f"Expected total market cap of 300.0, got {total_market_cap}."


@patch('src.main.yf.Ticker')
@patch('src.main.yf.download')
def test_fetch_and_plot_exceed_company_limit(mock_download, mock_info):
    company_names = list(COMPANY_TICKERS.keys())[:8]  # Assuming COMPANY_TICKERS has at least 8 entries
    indicator_types = ['SMA']

    # Call the function
    images, error_message, total_market_cap = fetch_and_plot(company_names, indicator_types)

    # Verify results
    assert images is None, "Images should be None when company limit is exceeded."
    assert error_message == "Exceeded company limit", f"Expected error message 'Exceeded company limit', got '{error_message}'."
    assert total_market_cap is None, "Total market cap should be None when company limit is exceeded."


@patch('src.main.yf.Ticker')
@patch('src.main.yf.download')
def test_fetch_and_plot_multiple_indicators_multiple_companies(mock_download, mock_info):
    company_names = ['Enterprise Products Partners', 'Kinder Morgan']
    indicator_types = ['SMA', 'MACD']

    # Call the function
    images, error_message, total_market_cap = fetch_and_plot(company_names, indicator_types)

    # Verify results
    assert images is None, "Images should be None when multiple indicators are selected."
    assert error_message == "Multiple indicators not supported", f"Expected error message 'Multiple indicators not supported', got '{error_message}'."
    assert total_market_cap is None, "Total market cap should be None when multiple indicators are selected."