#file generated at 2026-06-06 01:07:34
from importlib import import_module
from datetime import date, datetime, timedelta

TABLE_A_CURRENCIES = frozenset({'MXN', 'LVL', 'CLP', 'HUF', 'AUD', 'THB', 'EUR', 'BRL', 'UAH', 'RON', 'ILS', 'NOK', 'SGD', 'HRK', 'ZAR', 'JPY', 'BGN', 'NZD', 'USD', 'TRY', 'CNY', 'ISK', 'XDR', 'CHF', 'KRW', 'IDR', 'CAD', 'PHP', 'HKD', 'CZK', 'DKK', 'RUB', 'MYR', 'SEK', 'LTL', 'INR', 'GBP'})
TABLE_B_CURRENCIES = frozenset({'SLE', 'FJD', 'KWD', 'XOF', 'KHR', 'NIO', 'PGK', 'XAF', 'CVE', 'ANG', 'VEF', 'NPR', 'VUV', 'LAK', 'BBD', 'ZWL', 'SAR', 'ETB', 'YER', 'BWP', 'GEL', 'TND', 'HTG', 'IRR', 'PAB', 'CDF', 'PEN', 'MMK', 'BHD', 'MRO', 'GYD', 'XPF', 'MUR', 'RSD', 'CRC', 'UYU', 'MVR', 'SDG', 'STD', 'MKD', 'LYD', 'MZN', 'TMT', 'BAM', 'TOP', 'SYP', 'PYG', 'SOS', 'BYN', 'MOP', 'BND', 'OMR', 'SSP', 'SCR', 'SLL', 'AFN', 'GNF', 'GIP', 'DOP', 'RWF', 'XCG', 'BZD', 'BOB', 'AWG', 'TWD', 'ALL', 'GTQ', 'QAR', 'COP', 'TTD', 'DJF', 'EGP', 'ZWG', 'GHS', 'PKR', 'GMD', 'DZD', 'NAD', 'KMF', 'SZL', 'LSL', 'RUB', 'MNT', 'MRU', 'WST', 'UGX', 'CUP', 'STN', 'UZS', 'ERN', 'SVC', 'KGS', 'LKR', 'BDT', 'VES', 'SRD', 'VND', 'MWK', 'JMD', 'MGA', 'KES', 'TZS', 'KZT', 'ZMK', 'AED', 'ARS', 'AZN', 'MAD', 'XCD', 'AMD', 'BIF', 'BSD', 'SBD', 'LBP', 'AOA', 'TJS', 'BYR', 'NGN', 'JOD', 'ZMW', 'HNL', 'MDL', 'LRD', 'IQD'})

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

    if currency == 'USD' or currency == 'EUR': table_name = 'A'
    elif currency in TABLE_A_CURRENCIES: table_name = 'A'
    elif currency in TABLE_B_CURRENCIES: table_name = 'B'
    else: raise ValueError('Error - wrong currency')

    if date_given > date(2026,6,5):
        from .online_fetcher import fetch_rate_from_nbp
        rate = fetch_rate_from_nbp(date_given, currency, table_name)
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
