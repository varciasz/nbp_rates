#file generated at 2026-06-11 05:35:57
from importlib import import_module
from datetime import date, datetime, timedelta

TABLE_A_CURRENCIES = frozenset({'BRL', 'CAD', 'SKK', 'ILS', 'IRR', 'XDR', 'FIM', 'PTE', 'CYP', 'ZAR', 'LUC', 'YUN', 'MTL', 'CNY', 'ESP', 'CHF', 'HKD', 'KWD', 'HRK', 'EUR', 'LBP', 'BEF', 'INR', 'DKK', 'LYD', 'PHP', 'BEC', 'YUD', 'USD', 'RON', 'ITL', 'NZD', 'MYR', 'IDR', 'BEL', 'GBP', 'LUL', 'SGD', 'GRD', 'SEK', 'NOK', 'ATS', 'XEU', 'TRL', 'LTL', 'IEP', 'LVL', 'NLG', 'UAH', 'KRW', 'EEK', 'SAR', 'RUB', 'ISK', 'BGN', 'FRF', 'SIT', 'MXN', 'THB', 'TRY', 'CLP', 'DEM', 'AUD', 'JPY', 'HUF', 'LUF', 'CZK'})
TABLE_B_CURRENCIES = frozenset({'CVE', 'PYG', 'SKK', 'DJF', 'SSP', 'DOP', 'KMF', 'XPF', 'SLL', 'MVR', 'CNY', 'MUR', 'SLE', 'ZRN', 'GTQ', 'MWK', 'CRC', 'MKD', 'RSD', 'KES', 'NZD', 'IDR', 'MYR', 'BND', 'XCG', 'NPR', 'ECS', 'TJS', 'CDF', 'EEK', 'GMD', 'PKR', 'NAD', 'ROL', 'WST', 'AFA', 'GIP', 'AWG', 'TRY', 'GHC', 'ZWG', 'BAM', 'PAB', 'MZM', 'ALL', 'STN', 'GEL', 'ILS', 'MZN', 'BOB', 'VND', 'MGF', 'MRO', 'SVC', 'ZAR', 'FJD', 'MRU', 'KGS', 'KWD', 'ARS', 'BGL', 'BYB', 'GNF', 'BYN', 'SDD', 'VEF', 'TOP', 'ZMK', 'AMD', 'SZL', 'DZD', 'UYU', 'SAR', 'ISK', 'BDT', 'AOA', 'BGN', 'MAD', 'COP', 'EGP', 'NIO', 'BSD', 'CLP', 'JMD', 'SRG', 'BIF', 'KZT', 'BBD', 'BRL', 'NGN', 'OMR', 'AZN', 'STD', 'IRR', 'IQD', 'BHD', 'KHR', 'CSD', 'ERN', 'GHS', 'YER', 'HTG', 'QAR', 'SCR', 'UZS', 'PHP', 'JOD', 'XCD', 'RWF', 'SGD', 'MDL', 'PGK', 'ETB', 'LTL', 'LVL', 'UAH', 'TZS', 'BYR', 'THB', 'SOS', 'ANG', 'SYP', 'ZWR', 'TND', 'ZWL', 'VES', 'UGX', 'TMT', 'CYP', 'GYD', 'BZD', 'MTL', 'ZMW', 'SBD', 'VEB', 'VUV', 'HKD', 'XAF', 'YUM', 'HRK', 'MNT', 'LBP', 'INR', 'LYD', 'MGA', 'RON', 'AFN', 'BWP', 'SRD', 'ZWD', 'LSL', 'CUP', 'LAK', 'MMK', 'KRW', 'TRL', 'SDG', 'AED', 'RUB', 'HNL', 'AON', 'MXN', 'SIT', 'LRD', 'TTD', 'TWD', 'XOF', 'PEN', 'LKR', 'MOP'})

def ProvideCurrencyRate(date_given, currency, fallback=False, _depth=0):
    """
    Fetches FX rate for a given date. If rate is not found and fallback is True,
    it searches recursively up to 31 days back (to support Table B and holidays).
    Data since 2012 till 2026-6-10 is available offline but if provided date is more recent then nbp api is used
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

    if date_given > date(2026,6,10):
        if currency == 'USD' or currency == 'EUR': table_name = 'A'
        elif currency in TABLE_A_CURRENCIES: table_name = 'A'
        elif currency in TABLE_B_CURRENCIES: table_name = 'B'
        else: raise ValueError('Error - wrong currency')

        from .online_fetcher import fetch_rate_from_nbp
        rate = fetch_rate_from_nbp(date_given, currency, table_name)
        if rate == '-1' and currency in {'BRL', 'SKK', 'ILS', 'IRR', 'CYP', 'ZAR', 'MTL', 'CNY', 'HKD', 'KWD', 'HRK', 'LBP', 'INR', 'PHP', 'LYD', 'RON', 'NZD', 'IDR', 'MYR', 'SGD', 'UAH', 'TRL', 'LTL', 'LVL', 'KRW', 'EEK', 'SAR', 'RUB', 'ISK', 'BGN', 'SIT', 'MXN', 'THB', 'TRY', 'CLP'}:  # some currencies are in both tables
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
