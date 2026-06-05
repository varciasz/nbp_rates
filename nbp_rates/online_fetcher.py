import urllib.request
import urllib.error
import json
import datetime

def fetch_rate_from_nbp(date_given: datetime.date, currency: str, table_name: str) -> str:
    """
    Fetch a specific exchange rate from the NBP Web API using only the standard library.
    """
    # https://api.nbp.pl/   description of API - https://api.nbp.pl/en.html#api-description
    # NBP API expects YYYY-MM-DD format
    formatted_date = date_given.strftime("%Y-%m-%d")
    
    # Construct the URL
    url = f"https://api.nbp.pl/api/exchangerates/rates/{table_name}/{currency}/{formatted_date}/?format=json"
    
    # Define headers to mimic a browser (good practice to avoid blocks)
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        req = urllib.request.Request(url, headers=headers)
        
        # Using context manager to ensure the connection is closed
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.getcode() == 200:
                data = json.loads(response.read().decode('utf-8'))
                # Extract the 'mid' rate
                # The structure is: {"rates": [{"mid": 1.234, ...}], ...}
                rates_list = data.get('rates', [])
                if rates_list:
                    rate_value = rates_list[0].get('mid', '-1')
                    return str(rate_value)
        return "-1"

    except urllib.error.HTTPError as e:
        # 404 is returned by NBP if there is no data for a specific day
        return "-1"
    except (urllib.error.URLError, TimeoutError):
        # Network issues, DNS issues, or timeouts
        return "-1"
    except (json.JSONDecodeError, KeyError, IndexError):
        # Unexpected response format
        return "-1"