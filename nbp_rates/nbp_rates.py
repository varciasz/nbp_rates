#file generated at 2026-07-10 01:51:55
from importlib import import_module
from datetime import date, datetime, timedelta

TABLE_A_CURRENCIES = frozenset(['ATS', 'AUD', 'BEC', 'BEF', 'BEL', 'BGN', 'BRL', 'CAD', 'CHF', 'CLP', 'CNY', 'CYP', 'CZK', 'DEM', 'DKK', 'EEK', 'ESP', 'EUR', 'FIM', 'FRF', 'GBP', 'GRD', 'HKD', 'HRK', 'HUF', 'IDR', 'IEP', 'ILS', 'INR', 'IRR', 'ISK', 'ITL', 'JPY', 'KRW', 'KWD', 'LBP', 'LTL', 'LUC', 'LUF', 'LUL', 'LVL', 'LYD', 'MTL', 'MXN', 'MYR', 'NLG', 'NOK', 'NZD', 'PHP', 'PTE', 'RON', 'RUB', 'SAR', 'SEK', 'SGD', 'SIT', 'SKK', 'THB', 'TRL', 'TRY', 'UAH', 'USD', 'XDR', 'XEU', 'YUD', 'YUN', 'ZAR'])
TABLE_B_CURRENCIES = frozenset(['AED', 'AFA', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'AON', 'ARS', 'AWG', 'AZN', 'BAM', 'BBD', 'BDT', 'BGL', 'BGN', 'BHD', 'BIF', 'BND', 'BOB', 'BRL', 'BSD', 'BWP', 'BYB', 'BYN', 'BYR', 'BZD', 'CDF', 'CLP', 'CNY', 'COP', 'CRC', 'CSD', 'CUP', 'CVE', 'CYP', 'DJF', 'DOP', 'DZD', 'ECS', 'EEK', 'EGP', 'ERN', 'ETB', 'FJD', 'GEL', 'GHC', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HRK', 'HTG', 'IDR', 'ILS', 'INR', 'IQD', 'IRR', 'ISK', 'JMD', 'JOD', 'KES', 'KGS', 'KHR', 'KMF', 'KRW', 'KWD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LTL', 'LVL', 'LYD', 'MAD', 'MDL', 'MGA', 'MGF', 'MKD', 'MMK', 'MNT', 'MOP', 'MRO', 'MRU', 'MTL', 'MUR', 'MVR', 'MWK', 'MXN', 'MYR', 'MZM', 'MZN', 'NAD', 'NGN', 'NIO', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 'PGK', 'PHP', 'PKR', 'PYG', 'QAR', 'ROL', 'RON', 'RSD', 'RUB', 'RWF', 'SAR', 'SBD', 'SCR', 'SDD', 'SDG', 'SGD', 'SIT', 'SKK', 'SLE', 'SLL', 'SOS', 'SRD', 'SRG', 'SSP', 'STD', 'STN', 'SVC', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TOP', 'TRL', 'TRY', 'TTD', 'TWD', 'TZS', 'UAH', 'UGX', 'UYU', 'UZS', 'VEB', 'VEF', 'VES', 'VND', 'VUV', 'WST', 'XAF', 'XCD', 'XCG', 'XOF', 'XPF', 'YER', 'YUM', 'ZAR', 'ZMK', 'ZMW', 'ZRN', 'ZWD', 'ZWG', 'ZWL', 'ZWR'])

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
        if rate == '-1' and currency in ['BGN', 'BRL', 'CLP', 'CNY', 'CYP', 'EEK', 'HKD', 'HRK', 'IDR', 'ILS', 'INR', 'IRR', 'ISK', 'KRW', 'KWD', 'LBP', 'LTL', 'LVL', 'LYD', 'MTL', 'MXN', 'MYR', 'NZD', 'PHP', 'RON', 'RUB', 'SAR', 'SGD', 'SIT', 'SKK', 'THB', 'TRL', 'TRY', 'UAH', 'ZAR']:  # some currencies are in both tables
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
