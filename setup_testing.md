To ensure the reliability and maintainability of your Python application, it's essential to implement comprehensive testing and a proper setup for your Git repository. Below, you'll find a detailed guide on setting up tests using `pytest`, configuring the repository structure, and ensuring all components are adequately tested.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Dependencies](#dependencies)
3. [Testing with Pytest](#testing-with-pytest)
    - [Test Configuration](#test-configuration)
    - [Mocking External Dependencies](#mocking-external-dependencies)
    - [Writing Tests](#writing-tests)
        - [Testing `fetch_historical_data`](#testing-fetch_historical_data)
        - [Testing `plot_to_image`](#testing-plot_to_image)
        - [Testing `plot_indicator`](#testing-plot_indicator)
        - [Testing `plot_indicators`](#testing-plot_indicators)
        - [Testing `select_all_indicators`](#testing-select_all_indicators)
        - [Testing Gradio App Components](#testing-gradio-app-components)
4. [Continuous Integration (CI)](#continuous-integration-ci)
5. [Running the Tests](#running-the-tests)
6. [Additional Considerations](#additional-considerations)

---

## Project Structure

Organizing your repository systematically helps in maintaining and scaling the project. Here's a recommended structure:

```
your-repo/
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   ├── __init__.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_fetch_historical_data.py
│   ├── test_plot_to_image.py
│   ├── test_plot_indicator.py
│   ├── test_plot_indicators.py
│   ├── test_select_all_indicators.py
│   └── test_gradio_app.py
├── requirements.txt
├── requirements-dev.txt
├── setup.py
└── README.md
```

- **src/**: Contains your main application code.
- **tests/**: Contains all test modules.
- **requirements.txt**: Lists runtime dependencies.
- **requirements-dev.txt**: Lists development dependencies, including testing tools.
- **setup.py**: Setup script for your project.
- **.github/workflows/**: Contains CI workflow configurations.

## Dependencies

### Runtime Dependencies (`requirements.txt`)

Ensure all necessary packages for running the application are listed here.

```txt
yfinance
matplotlib
numpy
Pillow
gradio
cachetools
```

### Development Dependencies (`requirements-dev.txt`)

Include packages required for development and testing.

```txt
pytest
pytest-mock
pytest-cov
mock
```

Install them using:

```bash
pip install -r requirements-dev.txt
```

## Testing with Pytest

We'll use `pytest` as the testing framework due to its simplicity and powerful features.

### Test Configuration

Create a `conftest.py` file in the `tests/` directory to define fixtures and configurations shared across multiple test modules.

**`tests/conftest.py`**

```python
import pytest
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
```

### Mocking External Dependencies

To ensure tests are deterministic and do not rely on external APIs, we'll mock `yfinance` calls.

### Writing Tests

#### Testing `fetch_historical_data`

**`tests/test_fetch_historical_data.py`**

```python
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
    assert market_cap == 'N/A'
```

#### Testing `plot_to_image`

**`tests/test_plot_to_image.py`**

```python
import pytest
from src.main import plot_to_image
import matplotlib.pyplot as plt

def test_plot_to_image():
    plt.plot([1, 2, 3], [4, 5, 6], label='Test Line')
    title = "Test Plot"
    market_cap = 100.5
    
    image = plot_to_image(plt, title, market_cap)
    
    assert image is not None
    assert image.format == 'PNG'
    assert image.size != (0, 0)
```

#### Testing `plot_indicator`

**`tests/test_plot_indicator.py`**

```python
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
```

#### Testing `plot_indicators`

**`tests/test_plot_indicators.py`**

```python
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
```

#### Testing `select_all_indicators`

**`tests/test_select_all_indicators.py`**

```python
import pytest
from src.main import select_all_indicators

def test_select_all_indicators_true():
    select_all = True
    indicators = select_all_indicators(select_all)
    expected = ["SMA", "MACD", "RSI", "Bollinger Bands"]
    assert indicators == expected

def test_select_all_indicators_false():
    select_all = False
    indicators = select_all_indicators(select_all)
    expected = []
    assert indicators == expected
```

#### Testing Gradio App Components

Testing UI components can be more involved. We'll focus on testing the backend functions that the UI interacts with.

**`tests/test_gradio_app.py`**

```python
import pytest
from src.main import fetch_and_plot, select_all_indicators
from unittest.mock import patch

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
    assert error_message == "You can only select one indicator when selecting multiple companies."
    assert total_market_cap is None
```

## Continuous Integration (CI)

Integrate testing into your CI pipeline to ensure tests run automatically on each commit or pull request. Here's an example using GitHub Actions.

**`.github/workflows/ci.yml`**

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt

    - name: Run tests
      run: |
        pytest --cov=src tests/

    - name: Upload coverage to Coveralls
      uses: coverallsapp/github-action@v3
      with:
        github-token: ${{ secrets.GITHUB_TOKEN }}
```

**Notes:**

- **Coverage Reporting:** The `--cov=src` flag generates coverage reports. Integrate with services like Coveralls or Codecov for detailed insights.
- **Secrets:** Ensure necessary secrets (e.g., API keys) are securely stored in GitHub Secrets if needed.

## Running the Tests

1. **Install Dependencies:**

   Ensure you have Python installed (preferably 3.8+). Install the required packages:

   ```bash
   pip install -r requirements-dev.txt
   ```

2. **Run Pytest:**

   Execute the tests using `pytest`:

   ```bash
   pytest
   ```

   For coverage reports:

   ```bash
   pytest --cov=src tests/
   ```

3. **View Test Results:**

   `pytest` will output the test results, indicating passed, failed, or skipped tests along with any assertion messages.

## Additional Considerations

- **Test Coverage:** Aim for high test coverage, especially for critical functions. Use coverage tools to identify untested parts of your code.
  
  ```bash
  pytest --cov=src tests/
  ```

- **Edge Cases:** Ensure tests cover edge cases, such as empty data, invalid inputs, and exceptions.

- **Performance Testing:** While not covered here, consider adding performance tests if certain functions are critical for application performance.

- **Documentation:** Document your tests and testing strategy in your `README.md` to help future contributors understand how to run and write tests.

- **Linting and Formatting:** Integrate tools like `flake8` or `black` to maintain code quality and consistency.

