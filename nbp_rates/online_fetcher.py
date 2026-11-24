import urllib.request
import urllib.error
import json
import datetime
import os
import time
from typing import Optional


RETRY_DELAY_SECONDS = 0.25

def fetch_rate_from_nbp(date_given: datetime.date, currency: str, table_name: str, MAX_ATTEMPTS: Optional[int] = None) -> str:
    """
    Fetch a specific exchange rate from the NBP Web API using only the standard library.
    MAX_ATTEMPTS is the total number of attempts for transient failures. By default,
    use 10 attempts in GitHub Actions and 3 elsewhere.
    """
    if MAX_ATTEMPTS is None:
        MAX_ATTEMPTS = 10 if os.environ.get("GITHUB_ACTIONS") == "true" else 3
    if not isinstance(MAX_ATTEMPTS, int) or isinstance(MAX_ATTEMPTS, bool) or MAX_ATTEMPTS < 1:
        raise ValueError("MAX_ATTEMPTS must be a positive integer")

    # https://api.nbp.pl/   description of API - https://api.nbp.pl/en.html#api-description
    # NBP API expects YYYY-MM-DD format
    formatted_date = date_given.strftime("%Y-%m-%d")
    
    # Construct the URL
    url = f"https://api.nbp.pl/api/exchangerates/rates/{table_name}/{currency}/{formatted_date}/?format=json"
    
    # Define headers to mimic a browser (good practice to avoid blocks)
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    req = urllib.request.Request(url, headers=headers)

    for attempt in range(MAX_ATTEMPTS):
        try:
            # Using context manager to ensure the connection is closed
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.getcode() == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    rates_list = data.get('rates', [])
                    if rates_list:
                        rate_value = rates_list[0].get('mid', '-1')
                        return str(rate_value)
            return "-1"

        except urllib.error.HTTPError as error:
            # 404 means that no table entry exists for this date.
            if error.code == 404:
                return "-1"
        except (urllib.error.URLError, TimeoutError):
            pass
        except (json.JSONDecodeError, KeyError, IndexError):
            return "-1"

        if attempt < MAX_ATTEMPTS - 1:
            time.sleep(RETRY_DELAY_SECONDS * (attempt + 1))

    return "-1"