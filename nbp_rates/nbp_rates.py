#file generated at 2026-06-05 20:24:16
from importlib import import_module
from datetime import date, datetime, timedelta

TABLE_A_CURRENCIES = frozenset({'SEK', 'MXN', 'RON', 'LTL', 'ILS', 'IDR', 'XDR', 'NZD', 'THB', 'INR', 'HRK', 'MYR', 'BRL', 'LVL', 'ZAR', 'DKK', 'GBP', 'TRY', 'CLP', 'CNY', 'NOK', 'RUB', 'CZK', 'SGD', 'UAH', 'EUR', 'ISK', 'CAD', 'HUF', 'BGN', 'KRW', 'HKD', 'AUD', 'CHF', 'PHP', 'JPY', 'USD'})
TABLE_B_CURRENCIES = frozenset({'ZWL', 'SAR', 'XAF', 'HNL', 'WST', 'NIO', 'GIP', 'HTG', 'KES', 'XPF', 'BYN', 'SZL', 'QAR', 'DJF', 'KWD', 'SVC', 'XCD', 'SSP', 'SYP', 'NAD', 'XOF', 'TZS', 'MAD', 'ERN', 'TND', 'SLL', 'SLE', 'RSD', 'KGS', 'KZT', 'BDT', 'LAK', 'COP', 'ZMW', 'YER', 'PEN', 'PYG', 'CUP', 'BSD', 'VES', 'IQD', 'AFN', 'AMD', 'BIF', 'RWF', 'ALL', 'GMD', 'TJS', 'PAB', 'LRD', 'CRC', 'PGK', 'NPR', 'GNF', 'BYR', 'AED', 'GHS', 'VND', 'DZD', 'SBD', 'MDL', 'LYD', 'SCR', 'KMF', 'BAM', 'UYU', 'EGP', 'MKD', 'SRD', 'SDG', 'MRO', 'TOP', 'STN', 'MNT', 'JOD', 'CVE', 'PKR', 'MOP', 'OMR', 'UGX', 'JMD', 'ARS', 'AZN', 'VUV', 'GYD', 'BHD', 'TMT', 'MZN', 'GTQ', 'BZD', 'VEF', 'AWG', 'BOB', 'BBD', 'BND', 'BWP', 'CDF', 'LKR', 'ANG', 'LBP', 'MMK', 'LSL', 'KHR', 'ZMK', 'STD', 'ETB', 'UZS', 'MVR', 'MWK', 'TTD', 'MUR', 'GEL', 'DOP', 'RUB', 'XCG', 'MGA', 'FJD', 'TWD', 'IRR', 'AOA', 'ZWG', 'SOS', 'NGN', 'MRU'})

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
