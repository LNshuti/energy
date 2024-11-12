import pytest
from src.main import plot_indicator

def test_plot_indicator_sma(mock_yf_download, mock_yf_info, sample_data):
    company_name = 'Enterprise Products Partners'
    ticker = 'EPD'
    indicator = 'SMA'
    market_cap = 150.0
    
    image = plot_indicator(sample_data, company_name, ticker, indicator, market_cap)
    
    assert image is not None
    assert image.format == 'PNG'

def test_plot_indicator_macd(mock_yf_download, mock_yf_info, sample_data):
    company_name = 'Enterprise Products Partners'
    ticker = 'EPD'
    indicator = 'MACD'
    market_cap = 150.0
    
    image = plot_indicator(sample_data, company_name, ticker, indicator, market_cap)
    
    assert image is not None
    assert image.format == 'PNG'

def test_plot_indicator_rsi(mock_yf_download, mock_yf_info, sample_data):
    company_name = 'Enterprise Products Partners'
    ticker = 'EPD'
    indicator = 'RSI'
    market_cap = 150.0
    
    image = plot_indicator(sample_data, company_name, ticker, indicator, market_cap)
    
    assert image is not None
    assert image.format == 'PNG'

def test_plot_indicator_bollinger_bands(mock_yf_download, mock_yf_info, sample_data):
    company_name = 'Enterprise Products Partners'
    ticker = 'EPD'
    indicator = 'Bollinger Bands'
    market_cap = 150.0
    
    image = plot_indicator(sample_data, company_name, ticker, indicator, market_cap)
    
    assert image is not None
    assert image.format == 'PNG'
