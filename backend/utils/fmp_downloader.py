import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

import os
import requests
import pandas as pd

def safe_fmp_download(ticker):
    api_key = os.getenv("FMP_API_KEY")
    if not api_key:
        print("Missing FMP_API_KEY")
        return None

    url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?apikey={api_key}"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if "historical" not in data or len(data["historical"]) == 0:
            print(f"FMP returned no data for {ticker}")
            return None

        df = pd.DataFrame(data["historical"])
        df["date"] = pd.to_datetime(df["date"])
        df = df.set_index("date")
        df = df.rename(columns={"close": "Close"})

        return df.sort_index()

    except Exception as e:
        print(f"FMP error for {ticker}: {e}")
        return None
