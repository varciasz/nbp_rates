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
    ("20260227", "USD", "3.5804"),
    ("19840102", "AUD", "88.04"), ("19840102", "ATS", "5.0618"),
    ("19840102", "BEC", "1.7495"), ("19840102", "BEF", "-1"),
    ("19840102", "GRD", "0.9889"), ("19840102", "SEK", "12.18"),
    ("19840102", "XDR", "-1"), ("19840312", "INR", "10.1672"),
    ("19840312", "LBP", "20.47"), ("19840319", "INR", "10.14"),
    ("19840319", "ITL", "0.0684"), ("19860310", "ATS", "10.6456"),
    ("19860317", "ATS", "10.44"), ("19860324", "XDR", "-1"),
    ("19860401", "XDR", "192.15"), ("19871019", "LBP", "1.06"),
    ("19871026", "LBP", "0.7500"), ("19871026", "LUC", "8.0375"),
    ("19881227", "BEL", "-1"), ("19890102", "BEL", "13.4796"),
    ("19900101", "BEC", "269.1981"), ("19900101", "BEL", "269.2744"),
    ("19900101", "IRR", "130.9622"), ("19900101", "YUD", "0.0799"),
    ("19900101", "YUN", "-1"), ("19900108", "BEC", "263.00"),
    ("19900108", "BEL", "263.00"), ("19900108", "IRR", "131.00"),
    ("19900108", "LUC", "263.00"), ("19921231", "ESP", "137.7400"),
    ("19921231", "YUN", "21.00"), ("19921231", "GBP", "23846.00"),
    ("19930104", "USD", "15777"), ("19930104", "BEF", "476"),
    ("19930104", "JPY", "126.52"), ("19930104", "ITL", "10.69"),
    ("19940214", "BEF", "609"), ("19940214", "LUF", "609"),
    ("19940215", "BEF", "611.04"), ("19940215", "LUF", "611.04"),
    ("19941107", "AUD", "17443"), ("19941107", "CAD", "17209"),
    ("19941230", "ATS", "2223"),
    ("19950101", "USD", "2.430100"), ("19950101", "XDR", "3.537800"),
    ("19950101", "LUF", "0.07633500"), ("19950515", "FRF", "0.490000"),
    ("19950516", "ATS", "0.2383"), ("19951229", "ITL", "0.001558"),
    ("19960102", "DEM", "1.7255"), ("19960102", "IEP", "3.9621"),
    ("19970206", "FRF", "0.5390"), ("19970206", "ESP", "0.021508"),
    ("19970206", "NOK", "0.4635"), ("19980325", "USD", "3.4390"),
    ("19980325", "DKK", "0.4927"), ("19980325", "JPY", "0.026482"),
    ("19980325", "XDR", "4.6186"), ("19981231", "ITL", "0.002112"),
    ("19981231", "XDR", "4.9297"),
    ("19990101", "USD", "3.5025"), ("19990101", "EEK", "-1"),
    ("19990101", "HUF", "0.016213"), ("20000103", "EUR", "4.1650"),
    ("20000103", "EEK", "0.2673"), ("20000103", "XDR", "5.6839"),
    ("20020102", "PTE", "0.017705"), ("20020102", "DEM", "-1"),
    ("20020125", "NLG", "1.6515"), ("20020301", "ATS", "-1"),
    ("20020301", "BEF", "-1"), ("20020301", "FIM", "-1"),
    ("20020301", "FRF", "-1"), ("20020301", "GRD", "-1"),
    ("20020301", "ESP", "-1"), ("20020301", "PTE", "-1"),
    ("20020301", "ITL", "-1"), ("20021231", "USD", "3.8388"),
    ("20021231", "CZK", "0.1275"), ("20021231", "JPY", "0.032336"),
    ("20021231", "GBP", "6.1802"),
    ("20021231", "EUR", "4.0202"), ("20030102", "CAD", "2.4344"),
    ("20030409", "RUB", "0.1277"), ("20030409", "UAH", "0.7491"),
    ("20041231", "CZK", "0.1341"), ("20041231", "HUF", "0.016590"),
    ("20041231", "XDR", "4.6410"),
    ("20041231", "USD", "2.9904"), ("20041231", "NOK", "0.4950"),
    ("20050103", "USD", "3.0123"), ("20050103", "ZAR", "0.5323"),
    ("20050103", "SIT", "0.017007"), ("20061003", "AUD", "2.3226"),
    ("20061003", "JPY", "0.026436"), ("20061003", "BGN", "-1"),
    ("20061003", "RUB", "0.1162"), ("20070404", "EEK", "0.2461"),
    ("20070404", "SKK", "0.1149"), ("20070404", "BGN", "1.9689"),
    ("20070404", "MTL", "8.9723"), ("20070404", "RON", "1.1538"),
    ("20070404", "SIT", "-1"), ("20070404", "XDR", "4.3628"),
    ("20071231", "CYP", "6.1205"), ("20071231", "LTL", "1.0374"),
    ("20071231", "XDR", "3.8484"),
    ("20080102", "THB", "0.0731"), ("20080102", "AUD", "2.1629"),
    ("20080102", "HUF", "0.014220"), ("20080102", "EEK", "0.2299"),
    ("20090114", "SGD", "2.1032"), ("20090114", "CHF", "2.8001"),
    ("20090114", "GBP", "4.5442"), ("20090114", "ISK", "0.024756"),
    ("20090114", "SKK", "-1"), ("20101231", "HKD", "0.3813"),
    ("20101231", "NZD", "2.2966"), ("20101231", "EEK", "0.2531"),
    ("20101231", "SEK", "0.4415"), ("20101231", "BRL", "1.7861"),
    ("20101231", "IDR", "0.00033134"), ("20101231", "CNY", "0.4497"),
    ("20101231", "THB", "0.0987"), ("20101231", "EUR", "3.9603"),
    ("20101231", "NOK", "0.5071"), ("20101231", "ILS", "-1"),
    ("20101231", "MXN", "0.2393"), ("20110103", "NZD", "2.3188"),
    ("20110103", "CLP", "-1"), ("20110103", "IDR", "0.00032943"),
    ("20110103", "INR", "-1"), ("20110103", "KRW", "0.002651"),
    ("20110103", "XDR", "4.5948"), ("20110812", "CZK", "0.1714"),
    ("20110831", "CLP", "0.006167"), ("20110831", "BRL", "1.7982"),
    ("20110831", "MYR", "0.9618"), ("20111230", "CNY", "0.5428"),
    ("19981222", "ALL", "0.024714"), ("19981222", "DZD", "0.058431"),
    ("19981222", "AON", "0.00001346"), ("19981222", "AOA", "-1"),
    ("19981222", "ANG", "1.9330"), ("19981222", "SAR", "0.9221"),
    ("19981222", "ARS", "3.4614"), ("19981222", "AMD", "-1"),
    ("19981222", "BHD", "9.1777"), ("19981222", "BDT", "0.071340"),
    ("19981222", "BBD", "1.7203"), ("19981222", "XOF", "0.006200"),
    ("19981222", "BYB", "0.00001463"), ("19981222", "BOB", "0.6135"),
    ("19981222", "JMD", "0.0936"), ("19981222", "JOD", "4.8630"),
    ("19981222", "QAR", "0.9505"), ("19981222", "KZT", "0.041276"),
    ("19981222", "KES", "0.055582"), ("19981222", "ZRN", "0.00002516"),
    ("19981222", "LSL", "0.5835"), ("19981222", "MGF", "0.00066284"),
    ("19981222", "MOP", "0.4324"), ("19981222", "MUR", "0.1401"),
    ("19981222", "MMK", "0.5534"), ("19981222", "NGN", "0.1581"),
    ("19981222", "SYP", "0.0769"), ("19981222", "TOP", "2.1487"),
    ("19981222", "MZM", "0.00028034"), ("19981222", "CLP", "0.007352"),
    ("20021224", "RUB", "0.1218"), ("20030304", "AOA", "0.0604"),
    ("20030304", "BZD", "2.0311"), ("20030304", "SYP", "0.0870"),
    ("20030304", "TTD", "0.6438"), ("20030304", "YUM", "0.0682"),
    ("20030304", "GHC", "0.000482"), ("20030304", "NZD", "2.2271"),
    ("20030304", "VEB", "0.002504"), ("20030304", "INR", "0.083946"),
    ("20030304", "CLP", "0.005341"), ("20080625", "ZWD", "0.0000000002"),
    ("20111228", "XCD", "1.2511"), ("20111228", "SAR", "0.8956"),
    ("20111228", "BBD", "1.6794"), ("20111228", "GTQ", "0.4295"),
    ("20111228", "HNL", "0.1770"), ("20111228", "JOD", "4.7342"),
    ("20111228", "KGS", "0.0724"), ("20111228", "CDF", "0.003627"),
    ("20111228", "SVC", "0.3840"), ("20111228", "SLL", "0.000763"),
    ("20111228", "SZL", "0.4125"), ("20111228", "STD", "0.00017885"),
    ("20111228", "AED", "0.9144"), ("20111228", "YUM", "-1")
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

#tests for online fetching funtion (do require internet connection and may fail if NBP API is down or if there are network issues)
#test is directly calling fetch_rate_from_nbp() function and comparing to the result of ProvideCurrencyRate() with fallback=False 
# testing first 20 cases from TEST_CASES
@pytest.mark.parametrize("date_str, currency, expected", TEST_CASES[:30])
def test_online_fetching(date_str, currency, expected):
    from nbp_rates.online_fetcher import fetch_rate_from_nbp
    date_obj = datetime.datetime.strptime(date_str, "%Y%m%d").date()
    online_result = fetch_rate_from_nbp(date_obj, currency, 'A')  # Try Table A first
    if online_result == '-1':  # If not found in Table A, try Table B
        online_result = fetch_rate_from_nbp(date_obj, currency, 'B')
    
    # Get the result from the library (which may use offline data or fallback)
    library_result = ProvideCurrencyRate(date_obj, currency, fallback=False)
    #eliminate zeroes at the end if result contains a decimal point (to match the format of online result)
    library_result = library_result.rstrip('0').rstrip('.') if '.' in library_result else library_result
    
    assert online_result == library_result, f"Online fetching mismatch for {currency} on {date_str}. Online: {online_result}, Library: {library_result}"