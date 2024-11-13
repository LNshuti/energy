import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import pytest
from src.main import fetch_and_plot, select_all_indicators
from unittest.mock import patch
from main import fetch_and_plot, select_all_indicators

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
    assert error_message == "Multiple indicators not supported"
    assert total_market_cap is None