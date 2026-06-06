#file generated at 2026-06-06 05:24:02
from importlib import import_module
from datetime import date, datetime, timedelta

TABLE_A_CURRENCIES = frozenset({'HUF', 'DKK', 'NOK', 'THB', 'NZD', 'KRW', 'BRL', 'LVL', 'SEK', 'MYR', 'USD', 'RUB', 'JPY', 'UAH', 'MXN', 'RON', 'CAD', 'CLP', 'ZAR', 'HRK', 'BGN', 'AUD', 'IDR', 'HKD', 'LTL', 'INR', 'PHP', 'SGD', 'TRY', 'ISK', 'EUR', 'CZK', 'XDR', 'GBP', 'CNY', 'ILS', 'CHF'})
TABLE_B_CURRENCIES = frozenset({'KMF', 'BND', 'VEF', 'MKD', 'LYD', 'SCR', 'VUV', 'AOA', 'ERN', 'RSD', 'KHR', 'XCG', 'BIF', 'NIO', 'PYG', 'BDT', 'TJS', 'PAB', 'TWD', 'GNF', 'CRC', 'SOS', 'TZS', 'RWF', 'BYR', 'ANG', 'WST', 'LAK', 'XCD', 'AMD', 'BAM', 'NPR', 'ZMW', 'BSD', 'AWG', 'CUP', 'SZL', 'ARS', 'HNL', 'MGA', 'ZWG', 'GTQ', 'JOD', 'ALL', 'KGS', 'CVE', 'PKR', 'AZN', 'VND', 'DOP', 'IRR', 'HTG', 'LKR', 'SLL', 'SLE', 'SAR', 'XOF', 'SDG', 'KWD', 'BOB', 'MNT', 'XPF', 'ZWL', 'MRO', 'JMD', 'MWK', 'UZS', 'SRD', 'SYP', 'TND', 'MDL', 'PEN', 'GMD', 'STD', 'LRD', 'KES', 'MRU', 'BWP', 'CDF', 'KZT', 'FJD', 'LSL', 'BHD', 'XAF', 'PGK', 'SSP', 'GHS', 'ETB', 'TTD', 'MAD', 'MMK', 'NGN', 'GIP', 'BZD', 'VES', 'STN', 'IQD', 'UYU', 'NAD', 'TMT', 'GEL', 'SVC', 'MUR', 'AED', 'EGP', 'RUB', 'MOP', 'COP', 'TOP', 'QAR', 'YER', 'DJF', 'ZMK', 'MVR', 'GYD', 'LBP', 'MZN', 'OMR', 'BBD', 'AFN', 'SBD', 'BYN', 'DZD', 'UGX'})

def ProvideCurrencyRate(date_given, currency, fallback=False, _depth=0):
    """
    Fetches FX rate for a given date. If rate is not found and fallback is True,
    it searches recursively up to 31 days back (to support Table B and holidays).
    Data since 2012 till 2026-6-5 is available offline but if provided date is more recent then nbp api is used
    """
    # Safety break for recursion (covers 31 days back)
    if _depth > 31: return '-1'

    if currency == 'PLN': return '1'

    if isinstance(date_given, datetime):
        date_given = date_given.date()
    elif isinstance(date_given, date):
        pass
    elif isinstance(date_given, str) and len(date_given) == 10 and date_given[4] == date_given[7] and date_given[:4].isdigit() and date_given[5:7].isdigit() and date_given[8:].isdigit():
        date_given = date(int(date_given[:4]), int(date_given[5:7]), int(date_given[8:]))
    else:
        raise ValueError('date_given must be a datetime.date object or a string in YYYY-MM-DD format')

    if date_given > date(2026,6,5):
        if currency == 'USD' or currency == 'EUR': table_name = 'A'
        elif currency in TABLE_A_CURRENCIES: table_name = 'A'
        elif currency in TABLE_B_CURRENCIES: table_name = 'B'
        else: raise ValueError('Error - wrong currency')

        from .online_fetcher import fetch_rate_from_nbp
        rate = fetch_rate_from_nbp(date_given, currency, table_name)
        if currency == 'RUB' and rate == '-1':  # RUB is in both tables and we want to fallback to the opposite table if rate is not found for the provided date (e.g. due to holidays or mid-year switch) - this logic is implemented in fetch_rate_from_nbp function
            rate = fetch_rate_from_nbp(date_given, currency, {'A': 'B', 'B': 'A'}[table_name]) #run also for the opposite table if rate is not found
    else:
        try:
            module = import_module(f'nbp_rates.currencies.curr_{currency.lower()}')
            rate = module.get_rate(date_given.year, date_given.month, date_given.day)
        except (ImportError, ModuleNotFoundError):
            return 'Error - unable to load currency module'

    # If rate is missing and fallback is enabled, try the previous day
    if fallback and rate == '-1':
        return ProvideCurrencyRate(date_given - timedelta(days=1), currency, fallback=True, _depth=_depth + 1)

    return rate
