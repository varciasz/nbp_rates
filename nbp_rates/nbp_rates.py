#file generated at 2026-07-08 03:34:28
from importlib import import_module
from datetime import date, datetime, timedelta

TABLE_A_CURRENCIES = frozenset({'HRK', 'XDR', 'DEM', 'TRL', 'YUD', 'NZD', 'SAR', 'LUF', 'CYP', 'HKD', 'LBP', 'KWD', 'LUC', 'EUR', 'LVL', 'MXN', 'KRW', 'BEF', 'SKK', 'MYR', 'ILS', 'MTL', 'ESP', 'PTE', 'RON', 'YUN', 'FRF', 'CNY', 'DKK', 'IRR', 'THB', 'SEK', 'CLP', 'ISK', 'LTL', 'SIT', 'BRL', 'IEP', 'RUB', 'GRD', 'SGD', 'LUL', 'IDR', 'XEU', 'FIM', 'ATS', 'HUF', 'INR', 'BGN', 'AUD', 'LYD', 'NOK', 'PHP', 'ITL', 'GBP', 'TRY', 'CAD', 'UAH', 'CZK', 'CHF', 'USD', 'BEL', 'BEC', 'JPY', 'EEK', 'NLG', 'ZAR'})
TABLE_B_CURRENCIES = frozenset({'BWP', 'GTQ', 'CDF', 'ZMK', 'GHC', 'UGX', 'KWD', 'YUM', 'SZL', 'SSP', 'MRO', 'NIO', 'TTD', 'KMF', 'MMK', 'TZS', 'AMD', 'MVR', 'ETB', 'PYG', 'LTL', 'SVC', 'BAM', 'OMR', 'GNF', 'IDR', 'XCG', 'MAD', 'HTG', 'RWF', 'RSD', 'XCD', 'FJD', 'MUR', 'GMD', 'LYD', 'MZM', 'TJS', 'TOP', 'VND', 'ZAR', 'QAR', 'NZD', 'CYP', 'KGS', 'XAF', 'LVL', 'XOF', 'JOD', 'COP', 'KRW', 'VEB', 'VEF', 'BHD', 'DJF', 'TND', 'ISK', 'MKD', 'SIT', 'HNL', 'RUB', 'MGA', 'KES', 'AZN', 'ANG', 'SCR', 'BGN', 'BIF', 'BZD', 'ZWR', 'DZD', 'GHS', 'SDG', 'ZWG', 'MOP', 'YER', 'BYB', 'CLP', 'TRL', 'SOS', 'LSL', 'LBP', 'AOA', 'MRU', 'ARS', 'BOB', 'LKR', 'LAK', 'ECS', 'MZN', 'ROL', 'MYR', 'BYR', 'MTL', 'RON', 'AED', 'IRR', 'AWG', 'SRD', 'AFA', 'TWD', 'EGP', 'ZMW', 'ZRN', 'PAB', 'BDT', 'SLE', 'XPF', 'STN', 'PKR', 'MDL', 'CVE', 'CSD', 'INR', 'GIP', 'ZWD', 'VUV', 'LRD', 'SRG', 'TRY', 'SDD', 'BBD', 'PGK', 'EEK', 'ERN', 'TMT', 'NGN', 'HRK', 'GEL', 'BND', 'MGF', 'DOP', 'SAR', 'CRC', 'HKD', 'MNT', 'ZWL', 'MXN', 'NPR', 'SYP', 'SKK', 'GYD', 'SLL', 'ILS', 'UZS', 'CNY', 'KZT', 'MWK', 'THB', 'WST', 'BRL', 'IQD', 'STD', 'NAD', 'BGL', 'SGD', 'PEN', 'JMD', 'BYN', 'VES', 'SBD', 'UYU', 'BSD', 'CUP', 'PHP', 'UAH', 'KHR', 'AFN', 'ALL', 'AON'})

def ProvideCurrencyRate(date_given, currency, fallback=False, _depth=0):
    """
    Fetches FX rate for a given date. If rate is not found and fallback is True,
    it searches recursively up to 31 days back (to support Table B and holidays).
    Data since 2012 till 2026-7-7 is available offline but if provided date is more recent then nbp api is used
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

    if date_given > date(2026,7,7):
        if currency == 'USD' or currency == 'EUR': table_name = 'A'
        elif currency in TABLE_A_CURRENCIES: table_name = 'A'
        elif currency in TABLE_B_CURRENCIES: table_name = 'B'
        else: raise ValueError('Error - wrong currency')

        from .online_fetcher import fetch_rate_from_nbp
        rate = fetch_rate_from_nbp(date_given, currency, table_name)
        if rate == '-1' and currency in {'HRK', 'TRL', 'NZD', 'SAR', 'CYP', 'HKD', 'LBP', 'KWD', 'MXN', 'LVL', 'KRW', 'SKK', 'MYR', 'ILS', 'MTL', 'RON', 'CNY', 'IRR', 'THB', 'ISK', 'LTL', 'SIT', 'BRL', 'RUB', 'SGD', 'IDR', 'INR', 'BGN', 'LYD', 'PHP', 'TRY', 'UAH', 'EEK', 'CLP', 'ZAR'}:  # some currencies are in both tables
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
