import pytest
import datetime
from nbp_rates.nbp_rates import ProvideCurrencyRate

# Test data provided by the user: (Date_String, Currency, Expected_Result)
TEST_CASES = [
    ("20120109", "USD", "3.5150"), ("20121107", "HKD", "0.4133"),
    ("20121129", "HUF", "0.014679"), ("20121231", "IDR", "0.00031765"),
    ("20130314", "AUD", "3.3104"), ("20140428", "MYR", "0.9300"),
    ("20140322", "USD", "-1"), ("20150629", "PHP", "0.0835"),
    ("20150712", "TRY", "-1"), ("20161014", "JPY", "0.037403"),
    ("20161119", "ISK", "-1"), ("20170531", "ISK", "0.037349"),
    ("20170806", "SEK", "-1"), ("20180104", "KRW", "0.003242"),
    ("20181230", "CLP", "-1"), ("20190116", "DKK", "0.5752"),
    ("20190511", "RON", "-1"), ("20201231", "EUR", "4.6148"),
    ("20200102", "JPY", "0.034910"), ("20210114", "MXN", "0.1888"),
    ("20210320", "XDR", "-1"), ("20220406", "SGD", "3.1348"),
    ("20220515", "UAH", "-1"), ("20230103", "IDR", "0.00028449"),
    ("20230503", "ZAR", "-1"), ("20241231", "GBP", "5.1488"),
    ("20241228", "NOK", "-1"), ("20250210", "CNY", "0.5551"),
    ("20250222", "CLP", "-1"), ("20260226", "EUR", "4.2224"),
    ("20260110", "NZD", "-1"), ("20120104", "PAB", "3.4320"),
    ("20120104", "CRC", "0.006788"), ("20120906", "SVC", "-1"),
    ("20120908", "GMD", "-1"), ("20131231", "MKD", "0.067495"),
    ("20140618", "AFN", "0.053974"), ("20151230", "BAM", "2.1690"),
    ("20151230", "VUV", "0.035150"), ("20160302", "LRD", "0.0441"),
    ("20160303", "MKD", "-1"), ("20170322", "CVE", "0.0387"),
    ("20181128", "AED", "1.0370"), ("20180207", "VES", "-1"),
    ("20180207", "VEF", "0.00013458"), ("20190911", "LRD", "0.0188"),
    ("20201028", "VES", "0.000008"), ("20201104", "VES", "0.00000755"),
    ("20211006", "VES", "0.00000095"), ("20211013", "VES", "0.9538"),
    ("20221026", "RWF", "0.004459"), ("20231220", "STN", "0.1751"),
    ("20240430", "ZWL", "0.000132"), ("20240508", "ZWL", "0.2944"),
    ("20250604", "ETB", "0.0275"), ("20260107", "MGA", "0.000780"),
    ("20260227", "USD", "3.5804")
]

# Relational fallback test cases: (Target_Date, Currency, Reference_Date)
# Logic: Result for Target_Date (with fallback=True) should match Reference_Date (exact)
FALLBACK_RELATIONAL_CASES = [
    ("20250209", "USD", "20250207"), # Sunday -> should match Friday
    ("20250208", "USD", "20250207"), # Saturday -> should match Friday
    ("20230503", "USD", "20230502"), # May 3rd (Holiday) -> should match May 2nd
    ("20200113", "VES", "20200108"), # Table B: Monday -> should match previous Wednesday
    ("20241228", "NOK", "20241227"), # Saturday -> should match Friday
    ("20260228", "USD", "20260227")  # Saturday -> should match Friday
]

DIFFERENT_DATE_FORMATS = [
    ("2025-02-22", datetime.date(2025, 2, 22), "CLP" ),
    ("2026-02-26", datetime.date(2026, 2, 26), "EUR" ),
    ("2012-01-04", datetime.date(2012, 1, 4), "PAB" ),
    ("2025.06.04", datetime.date(2025, 6, 4), "ETB" ),
    (datetime.datetime(2019, 1, 16,14,12), datetime.date(2019, 1, 16), "DKK" )
]


# List of inputs that should trigger a ValueError in ProvideCurrencyRate
INVALID_DATE_FORMATS = [
    "20260226",    # Lack of separator (nbp_rates.py expects YYYY-MM-DD)
    "26-02-2026",  # Wrong order
    "2026-02-31",  # Invalid day (Feb 31st)
    "not-a-date",  # Garbage string
    None,          # Wrong type
    12345678       # Wrong type
]

@pytest.mark.parametrize("bad_date", INVALID_DATE_FORMATS)
def test_invalid_date_formats(bad_date):
    """Verify that improper formats trigger a ValueError."""
    with pytest.raises(ValueError):
        ProvideCurrencyRate(bad_date, "USD")


@pytest.mark.parametrize("date_str, currency, expected", TEST_CASES)
def test_historical_rates(date_str, currency, expected):
    """Verify that generated library returns correct historical rates."""
    # Convert YYYYMMDD string to date object
    date_obj = datetime.datetime.strptime(date_str, "%Y%m%d").date()
    result = ProvideCurrencyRate(date_obj, currency, fallback=False)
    assert result == expected, f"Failed for {currency} on {date_str}. Expected {expected}, got {result}"




@pytest.mark.parametrize("date_str, date_date,currency", DIFFERENT_DATE_FORMATS)
def test_different_input_date(date_str, date_date, currency):
    assert ProvideCurrencyRate(date_str, currency) == ProvideCurrencyRate(date_date, currency), f"Failed for {currency} on {date_str}. Expected {ProvideCurrencyRate(date_date, currency)}, got {ProvideCurrencyRate(date_str, currency)}"




@pytest.mark.parametrize("target_str, currency, reference_str", FALLBACK_RELATIONAL_CASES)
def test_fallback_logic_relational(target_str, currency, reference_str):
    """
    Verify that fallback logic correctly returns the rate from the last available day.
    We compare the result of a 'missing' day with a known 'working' day.
    """
    # 1. Prepare date objects
    target_date = datetime.datetime.strptime(target_str, "%Y%m%d").date()
    reference_date = datetime.datetime.strptime(reference_str, "%Y%m%d").date()
    
    # 2. Get actual result (using fallback)
    actual_result = ProvideCurrencyRate(target_date, currency, fallback=True)
    
    # 3. Get expected result (exact rate from the reference day)
    expected_result = ProvideCurrencyRate(reference_date, currency, fallback=False)
    
    # 4. Perform assertions
    # Ensure we actually found a rate (not -1) and that both values are identical
    assert actual_result != "-1", f"Fallback failed to find any rate for {currency} starting from {target_str}"
    assert actual_result == expected_result, (
        f"Fallback mismatch for {currency}. "
        f"Date {target_str} (fallback) returned {actual_result}, "
        f"but reference date {reference_str} (exact) has {expected_result}"
    )