import pytest
from src.main import plot_indicators
import pandas as pd
from unittest.mock import patch

COMPANY_TICKERS = {
    'Energy Transfer LP': 'ET',
    'Enterprise Products Partners': 'EPD',
    'Kinder Morgan': 'KMI',
    'MPLX LP': 'MPLX',
    'Google': 'GOOGL',
    'Constellation Energy Corp': 'CEG',
    'Equitrans Midstream': 'ETRN',
    'Targa Resources': 'TRGP',
    'Western Midstream Partners': 'WES',
    'Williams Cos': 'WMB',
    'Chevron Corporation': 'CVX',
    'Loves': 'privately held',
    'Total Energies': 'TTE',
    'Exxon Mobil': 'XOM',
    'BP': 'BP',
    'Royal Dutch Shell': 'SHEL',
    'ConocoPhillips': 'COP',
    'Phillips 66': 'PSX',
    'Marathon Petroleum': 'MPC',
    'Cheniere Energy': 'LNG',
    'Devon Energy': 'DVN',
    'EOG Resources': 'EOG',
    'Pioneer Natural Resources': 'PXD',
    'Occidental Petroleum': 'OXY',
    'Hess Corporation': 'HES',
    'Antero Resources': 'AR',
    'Cabot Oil & Gas': 'COG',
    'Diamondback Energy': 'FANG',
    'Apache Corporation': 'APA',
    'Murphy Oil': 'MUR',
    'Noble Energy': 'NBL',
    'Range Resources': 'RRC',
    'Continental Resources': 'CLR',
    'Whiting Petroleum': 'WLL',
    'Parsley Energy': 'PE',
    'Cimarex Energy': 'XEC',
    'Marathon Oil': 'MRO',
    'National Oilwell Varco': 'NOV',
    'Schlumberger': 'SLB',
    'Halliburton': 'HAL',
    'Baker Hughes': 'BKR',
    'TechnipFMC': 'FTI',
    'Valero Energy': 'VLO',
    'HollyFrontier': 'HFC',
    'Tesoro Corporation': 'TSO',
    'Suncor Energy': 'SU',
    'Canadian Natural Resources': 'CNQ',
    'Imperial Oil': 'IMO',
    'Enbridge': 'ENB',
    'TC Energy': 'TRP',
    'Pembina Pipeline': 'PBA',
    'Keyera Corp': 'KEYUF'
}


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

# tests/test_plot_indicators.py

import pandas as pd
from unittest.mock import MagicMock, patch
import pytest
from src.main import plot_indicators  # Adjust the import path as necessary

@patch('src.main.fetch_historical_data')
def test_plot_indicators_with_no_data(mock_fetch_historical_data):
    # Mock fetch_historical_data to return (None, 'N/A') simulating no data available
    mock_fetch_historical_data.return_value = (None, 'N/A')
    
    company_names = ['Enterprise Products Partners']
    indicator_types = ['SMA']
    
    images, error_message, total_market_cap = plot_indicators(company_names, indicator_types)
    
    assert isinstance(images, list), "Expected images to be a list"
    assert len(images) == 0, "Expected no images for empty data"
    assert error_message == "No data available", f"Expected 'No data available', got '{error_message}'"
    assert total_market_cap is None, "Expected total_market_cap to be None"
