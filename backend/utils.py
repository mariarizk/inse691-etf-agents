import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def safe_eod_download(ticker, start="2018-01-01", end="2026-01-01"):
    api_key = os.getenv("EODHD_API_KEY")
    if not api_key:
        print("Missing EODHD_API_KEY")
        return None

    url = (
        f"https://eodhd.com/api/eod/{ticker}.US?"
        f"from={start}&to={end}&api_token={api_key}&fmt=json"
    )

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if not isinstance(data, list) or len(data) == 0:
            print(f"EODHD returned no data for {ticker}")
            return None

        df = pd.DataFrame(data)

        if "date" not in df.columns:
            print(f"EODHD error for {ticker}: missing 'date' field")
            return None

        df["date"] = pd.to_datetime(df["date"])
        df = df.set_index("date")

        df = df.rename(columns={
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "adjusted_close": "Adj Close",
            "volume": "Volume"
        })

        return df.sort_index()

    except Exception as e:
        print(f"EODHD error for {ticker}: {e}")
        return None
