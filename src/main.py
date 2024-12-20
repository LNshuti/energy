import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from PIL import Image
import io
import gradio as gr
from cachetools import cached, TTLCache
import cProfile
import pstats
import logging

logging.basicConfig(level=logging.DEBUG)

START_DATE = '2020-01-01'
END_DATE =  datetime.today().strftime('%Y-%m-%d')

# Global fontsize variable
FONT_SIZE = 32
# Company ticker mapping
COMPANY_TICKERS = {
    'Energy Transfer LP': 'ET',
    'Enterprise Products Partners': 'EPD',
    'Kinder Morgan': 'KMI',
    'MPLX LP': 'MPLX',
    'Constellation Energy Corp': 'CEG',
    'Targa Resources': 'TRGP',
    'Williams Cos': 'WMB',
    'Chevron Corporation': 'CVX',
    'Total Energies': 'TTE',
    'Exxon Mobil': 'XOM',
    'BP': 'BP',
    'Royal Dutch Shell': 'SHEL',
    'ConocoPhillips': 'COP',
    'Phillips 66': 'PSX',
    'Marathon Petroleum': 'MPC',
    'Cheniere Energy': 'LNG',
    'EOG Resources': 'EOG',
    'Occidental Petroleum': 'OXY',
    'Hess Corporation': 'HES',
    'Diamondback Energy': 'FANG',
    'Cimarex Energy': 'XEC',
    'Schlumberger': 'SLB',
    'Halliburton': 'HAL',
    'Baker Hughes': 'BKR',
    'Valero Energy': 'VLO',
    'Suncor Energy': 'SU',
    'Canadian Natural Resources': 'CNQ',
    'Imperial Oil': 'IMO',
    'Enbridge': 'ENB',
    'TC Energy': 'TRP',
    'Pembina Pipeline': 'PBA'
}

# Cache with 1-day TTL
cache = TTLCache(maxsize=100, ttl=86400)

@cached(cache)
def fetch_historical_data(ticker, start_date, end_date):
    """Fetch historical stock data and market cap from Yahoo Finance."""
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            raise ValueError(f"No data found for ticker {ticker}")
            return None, None
        info = yf.Ticker(ticker).info
        market_cap = info.get('marketCap', 'N/A')
        if market_cap != 'N/A':
            market_cap = market_cap / 1e9  # Convert to billions
        return data, market_cap
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None, 'N/A'

def plot_to_image(plt, title, market_cap):
    """Convert plot to a PIL Image object."""
    plt.title(title, fontsize=FONT_SIZE + 1, pad=40)
    plt.suptitle(f'Market Cap: ${market_cap:.2f} Billion', fontsize=FONT_SIZE - 5, y=0.92, weight='bold')
    plt.legend(fontsize=FONT_SIZE)
    plt.xlabel('Date', fontsize=FONT_SIZE)
    plt.ylabel('', fontsize=FONT_SIZE)
    plt.grid(True)
    plt.xticks(rotation=45, ha='right', fontsize=FONT_SIZE)
    plt.yticks(fontsize=FONT_SIZE)
    plt.tight_layout(rect=[0, 0, 1, 0.88])

    # Save plot to a PIL Image
    try:
        from io import BytesIO
        import PIL.Image

        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image = PIL.Image.open(buf)
        plt.close()
        return image
    except Exception as e:
        plt.close()
        return None

def plot_indicator(data, company_name, ticker, indicator, market_cap):
    """Plot selected technical indicator for a single company."""
    import pandas as pd
    if data is None or (isinstance(data, pd.DataFrame) and data.empty):
        logging.debug(f"No data to plot for {company_name} ({ticker}).")
        return None
    
    plt.figure(figsize=(10, 6))
    if indicator == "SMA":
        sma_55 = data['Close'].rolling(window=55).mean()
        sma_200 = data['Close'].rolling(window=200).mean()
        plt.plot(data.index, data['Close'], label='Close')
        plt.plot(data.index, sma_55, label='55-day SMA')
        plt.plot(data.index, sma_200, label='200-day SMA')
        plt.ylabel('Price', fontsize=FONT_SIZE)
    elif indicator == "MACD":
        exp1 = data['Close'].ewm(span=12, adjust=False).mean()
        exp2 = data['Close'].ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        plt.plot(data.index, macd, label='MACD')
        plt.plot(data.index, signal, label='Signal Line')
        plt.bar(data.index, macd - signal, label='MACD Histogram')
        plt.ylabel('MACD', fontsize=FONT_SIZE)
    elif indicator == "RSI":
        window_length = 14
        delta = data['Close'].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.ewm(alpha=1/window_length, min_periods=window_length).mean()
        avg_loss = loss.ewm(alpha=1/window_length, min_periods=window_length).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        plt.plot(data.index, rsi, label='RSI')
        plt.axhline(70, color='red', linestyle='--', label='Overbought (70)')
        plt.axhline(30, color='green', linestyle='--', label='Oversold (30)')
        plt.ylabel('RSI', fontsize=FONT_SIZE)
    elif indicator == "Bollinger Bands":
        window = 20
        no_of_std = 2
        rolling_mean = data['Close'].rolling(window).mean()
        rolling_std = data['Close'].rolling(window).std()
        upper_band = rolling_mean + (rolling_std * no_of_std)
        lower_band = rolling_mean - (rolling_std * no_of_std)
        plt.plot(data.index, data['Close'], label='Close Price')
        plt.plot(data.index, rolling_mean, label='20-day SMA', color='blue')
        plt.plot(data.index, upper_band, label='Upper Bollinger Band', color='green')
        plt.plot(data.index, lower_band, label='Lower Bollinger Band', color='red')
        plt.fill_between(data.index, lower_band, upper_band, color='grey', alpha=0.1)
        plt.ylabel('Price', fontsize=FONT_SIZE)

    return plot_to_image(plt, f'{company_name} ({ticker}) {indicator}', market_cap)

def plot_indicators(company_names, indicator_types):
    """Plot the selected indicators for the selected companies."""
    import pandas as pd
    images = []
    total_market_cap = 0.0
    
    # Validate input parameters
    if len(company_names) > 7:
        return None, "You can select up to 7 companies at the same time.", None
    if len(company_names) > 1 and len(indicator_types) > 1:
        return None, "You can only select one indicator when selecting multiple companies.", None

    try:
        with ThreadPoolExecutor() as executor:
            # Create futures for each company-indicator combination
            future_to_company = {
                executor.submit(
                    fetch_historical_data, 
                    COMPANY_TICKERS[company], 
                    START_DATE, 
                    END_DATE
                ): (company, indicator)
                for company in company_names
                for indicator in indicator_types
            }

            # Process completed futures
            for future in as_completed(future_to_company):
                company, indicator = future_to_company[future]
                ticker = COMPANY_TICKERS[company]
                data, market_cap = future.result()
                
                # Skip if no data or empty DataFrame
                if data is None or (isinstance(data, pd.DataFrame) and data.empty):
                    logging.debug(f"No data available for {ticker}. Skipping.")
                    continue
                    
                # Generate and store plot
                image = plot_indicator(data, company, ticker, indicator, market_cap)
                if image:
                    images.append(image)
                    if market_cap not in (None, 'N/A'):
                        total_market_cap += market_cap

        # Return appropriate response based on results
        if not images:
            return [], "No data available", None
        return images, "", total_market_cap

    except Exception as e:
        return [], str(e), None
    
def fetch_and_plot(company_names, indicator_types):
    """
    Fetch data and plot indicators for given companies
    """
    if len(company_names) > 7:
        return None, "Exceeded company limit", None
        
    if len(indicator_types) > 1:
        return None, "Multiple indicators not supported", None
        
    images = []
    total_market_cap = 0.0
    
    try:
        for company in company_names:
            ticker = COMPANY_TICKERS.get(company)
            if not ticker:
                continue
                
            data, market_cap = fetch_historical_data(ticker, START_DATE, END_DATE)
            if data is not None and market_cap != 'N/A':
                image = plot_indicator(data, company, ticker, indicator_types[0], market_cap)
                if image:
                    images.append(image)
                    total_market_cap += market_cap  # Remove the division here
            else:
                continue  # Handle cases where data or market_cap is not available
                    
        if not images:
            return [], "No data available", None
            
        return images, None, total_market_cap
        
    except Exception as e:
        return [], str(e), None
    
def select_all_indicators(select_all):
    """Select or deselect all indicators based on the select_all flag."""
    indicators = ["SMA", "MACD", "RSI", "Bollinger Bands"]
    return indicators if select_all else []

def launch_gradio_app():
    """Launch the Gradio app for interactive plotting."""
    company_choices = list(COMPANY_TICKERS.keys())
    indicators = ["SMA", "MACD", "RSI", "Bollinger Bands"]

    def fetch_and_plot(company_names, indicator_types):
        images, error_message, total_market_cap = plot_indicators(company_names, indicator_types)
        if error_message:
            return [None] * len(indicator_types), error_message, None
        return images, "", f"Total Market Cap: ${total_market_cap:.2f} Billion" if total_market_cap else "N/A"

    with gr.Blocks() as demo:
        company_checkboxgroup = gr.CheckboxGroup(choices=company_choices, label="Select Companies")
        
        select_all_checkbox = gr.Checkbox(label="Select All Indicators", value=False, interactive=True)
        indicator_types_checkboxgroup = gr.CheckboxGroup(choices=indicators, label="Select Technical Indicators")
        select_all_checkbox.change(select_all_indicators, inputs=select_all_checkbox, outputs=indicator_types_checkboxgroup)
        
        run_button = gr.Button("Plot Indicators")
        plot_gallery = gr.Gallery(label="Indicator Plots")
        error_markdown = gr.Markdown()
        market_cap_text = gr.Markdown()

        run_button.click(fetch_and_plot, inputs=[company_checkboxgroup, indicator_types_checkboxgroup], outputs=[plot_gallery, error_markdown, market_cap_text])

    demo.launch()

def profile_code():
    """Profile the main functions to find speed bottlenecks."""
    profiler = cProfile.Profile()
    profiler.enable()

    launch_gradio_app()

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats(10)

if __name__ == "__main__":
    profile_code()
