# nbp_rates

A modular Python library for providing NBP (Narodowy Bank Polski) exchange rates with both offline and online support.

## Features

- **Offline Support**: Includes historical exchange rates from 2012 to July 2026
- **Online Fallback**: Automatically fetches from NBP API for recent dates
- **Dual Table Support**: Supports both Table A (major currencies) and Table B (minor currencies)
- **Smart Fallback**: Optionally searches last available rate before given date (handles holidays, weekends and missing data)
- **Super Fast**: Optimized for speed with most queries served from local data with minimal API calls
- **Easy and Powerful**: Simple to use with 100+ currencies supported
- **Precise and exact output**: Results provided as string to avoid floating-point rounding issues
- **Flexible Date Input**: Accepts `datetime.date`, `datetime.datetime`, or ISO format strings (YYYY-MM-DD)
- **No external dependencies**: Pure Python with standard library

## Installation

Install from PyPI:

```bash
pip install nbp_rates
```

Or install in development mode from the repository:

```bash
git clone https://github.com/varciasz/nbp_rates.git
cd nbp_rates
pip install -e .
```

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## Usage

### Basic Usage

Get the exchange rate for a specific date and currency:

```python
from nbp_rates import ProvideCurrencyRate
from datetime import date

# Get USD rate for a specific date
rate = ProvideCurrencyRate(date(2024, 1, 15), 'USD')
print(f"USD rate on 2024-01-15: {rate}")

# Using a string date (ISO format)
rate = ProvideCurrencyRate('2024-01-15', 'EUR')
print(f"EUR rate on 2024-01-15: {rate}")

# Using datetime object
from datetime import datetime
rate = ProvideCurrencyRate(datetime(2024, 1, 15, 10, 30), 'GBP')
print(f"GBP rate on 2024-01-15: {rate}")
```

### Using Fallback

Enable fallback to search up to 31 days back for an available rate (useful for holidays, weekends and missing data):

```python
# Get rate for a holiday, falling back to previous business day if needed
rate = ProvideCurrencyRate(date(2024, 1, 1), 'USD', fallback=True)
print(f"USD rate: {rate}")
```

### Return Values

- Successfully fetched rate: String representation of the exchange rate (e.g., `"4.25"`)
- Currency not found: `"Error - wrong currency"`
- Module loading error: `"Error - unable to load currency module"`
- Fallback limit exceeded or rate not found: `"-1"`

### Supported Currencies

The library supports 100+ currencies including:

**Major currencies (Table A):**
USD, EUR, GBP, JPY, CHF, CAD, AUD, and many more

**Minor currencies (Table B):**
INR, CNY, MXN, BRL, ZAR, SGD, and many more

See the source code for the complete list of `TABLE_A_CURRENCIES` and `TABLE_B_CURRENCIES`.

## API Reference

### `ProvideCurrencyRate(date_given, currency, fallback=False, _depth=0)`

Fetches the FX rate for a given date and currency.

**Parameters:**
- `date_given` (datetime.date, datetime.datetime, or str): The date for which to fetch the rate
- `currency` (str): ISO 4217 currency code (e.g., 'USD', 'EUR')
- `fallback` (bool, optional): If True, searches up to 31 days back for available rates. Default: False
- `_depth` (int, optional): Internal parameter for recursion tracking. Default: 0

**Returns:**
- str: Exchange rate as a string, or error message

**Raises:**
- ValueError: If the date format is invalid or currency is not recognized

## Data Sources

- **Offline Data**: Embedded exchange rate data from 2012 to 2026-07-07
- **Online Data**: NBP API (`https://api.nbp.pl/`) for dates after the offline data cutoff

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Sebastian Kowalik

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Changelog

### Version 0.1.4
- Initial release with offline and online exchange rate support
