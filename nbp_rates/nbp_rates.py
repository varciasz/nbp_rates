#file generated at 2026-07-10 01:12:41
from importlib import import_module
from datetime import date, datetime, timedelta

TABLE_A_CURRENCIES = frozenset({'RON', 'UAH', 'ATS', 'NOK', 'SAR', 'LBP', 'XDR', 'KRW', 'PHP', 'HKD', 'EEK', 'KWD', 'DEM', 'SEK', 'ILS', 'IRR', 'CAD', 'PTE', 'LTL', 'MYR', 'ITL', 'BEF', 'SIT', 'ESP', 'LYD', 'BGN', 'NZD', 'GRD', 'BEC', 'CHF', 'CZK', 'ISK', 'USD', 'HRK', 'MXN', 'LUL', 'BEL', 'BRL', 'LVL', 'FIM', 'GBP', 'HUF', 'CYP', 'CNY', 'MTL', 'SGD', 'TRL', 'ZAR', 'FRF', 'YUN', 'THB', 'INR', 'SKK', 'IEP', 'IDR', 'CLP', 'LUF', 'LUC', 'XEU', 'TRY', 'DKK', 'RUB', 'AUD', 'JPY', 'NLG', 'YUD', 'EUR'})
TABLE_B_CURRENCIES = frozenset({'ZMK', 'AFA', 'AFN', 'ECS', 'SZL', 'SAR', 'KGS', 'ARS', 'MGA', 'MZN', 'RSD', 'AON', 'JOD', 'CUP', 'QAR', 'KWD', 'ZWL', 'MYR', 'SIT', 'LYD', 'BGN', 'NGN', 'WST', 'ISK', 'YER', 'MDL', 'BRL', 'BBD', 'SDG', 'KHR', 'TZS', 'LKR', 'ZAR', 'THB', 'IQD', 'PEN', 'SRD', 'KES', 'HNL', 'SSP', 'PAB', 'BND', 'BZD', 'LSL', 'CLP', 'TRY', 'AOA', 'YUM', 'BWP', 'GHC', 'KZT', 'RWF', 'TOP', 'TJS', 'UAH', 'CSD', 'EGP', 'TTD', 'PHP', 'HKD', 'DZD', 'MNT', 'ZRN', 'ILS', 'PKR', 'MRO', 'GYD', 'AWG', 'SBD', 'GMD', 'HRK', 'MXN', 'AMD', 'ETB', 'ROL', 'BYB', 'ERN', 'ZWR', 'SVC', 'CNY', 'MTL', 'ALL', 'SGD', 'KMF', 'TMT', 'UGX', 'XPF', 'SOS', 'SKK', 'VUV', 'MUR', 'SLE', 'TND', 'GNF', 'JMD', 'LVL', 'RON', 'OMR', 'KRW', 'GIP', 'FJD', 'BDT', 'BHD', 'HTG', 'UZS', 'IRR', 'GHS', 'SLL', 'SCR', 'DOP', 'NZD', 'BAM', 'MKD', 'GTQ', 'XCD', 'XOF', 'CYP', 'MZM', 'GEL', 'STN', 'INR', 'UYU', 'ZMW', 'STD', 'MRU', 'IDR', 'DJF', 'MWK', 'CRC', 'BYR', 'RUB', 'MMK', 'NPR', 'LAK', 'PGK', 'ZWD', 'LBP', 'BGL', 'CDF', 'AED', 'VEB', 'ZWG', 'EEK', 'MGF', 'SDD', 'NAD', 'LRD', 'ANG', 'BIF', 'LTL', 'PYG', 'AZN', 'XAF', 'BYN', 'COP', 'SYP', 'TWD', 'BSD', 'NIO', 'TRL', 'VES', 'VND', 'XCG', 'BOB', 'MOP', 'MVR', 'MAD', 'SRG', 'CVE', 'VEF'})

def ProvideCurrencyRate(date_given, currency, fallback=False, _depth=0):
    """
    Fetches FX rate for a given date. If rate is not found and fallback is True,
    it searches recursively up to 31 days back (to support Table B and holidays).
    Data since 2012 till 2026-7-9 is available offline but if provided date is more recent then nbp api is used
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

    if date_given > date(2026,7,9):
        if currency == 'USD' or currency == 'EUR': table_name = 'A'
        elif currency in TABLE_A_CURRENCIES: table_name = 'A'
        elif currency in TABLE_B_CURRENCIES: table_name = 'B'
        else: raise ValueError('Error - wrong currency')

        from .online_fetcher import fetch_rate_from_nbp
        rate = fetch_rate_from_nbp(date_given, currency, table_name)
        if rate == '-1' and currency in {'RON', 'UAH', 'SAR', 'LBP', 'KRW', 'PHP', 'HKD', 'EEK', 'KWD', 'ILS', 'IRR', 'LTL', 'MYR', 'SIT', 'LYD', 'BGN', 'NZD', 'ISK', 'HRK', 'MXN', 'BRL', 'CYP', 'CNY', 'MTL', 'SGD', 'TRL', 'ZAR', 'THB', 'INR', 'SKK', 'IDR', 'CLP', 'TRY', 'RUB', 'LVL'}:  # some currencies are in both tables
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
