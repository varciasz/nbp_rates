from .nbp_rates import ProvideCurrencyRate, TABLE_A_CURRENCIES, TABLE_B_CURRENCIES

__version__ = "1.7.20260904"

SupportedCurrencies = sorted(TABLE_A_CURRENCIES | TABLE_B_CURRENCIES)

__all__ = [
    "ProvideCurrencyRate",
    "SupportedCurrencies",
    "__version__"
]
