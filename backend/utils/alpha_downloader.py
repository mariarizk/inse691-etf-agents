import os
import requests
import pandas as pd

def safe_alpha_download(ticker):
    api_key = os.getenv("ALPHAVANTAGE_API_KEY")
    if not api_key:
        print("AlphaVantage: Missing API key.")
        return None

    url = (
        f"https://www.alphavantage.co/query?"
        f"function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&apikey={api_key}&outputsize=full"
    )

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if "Time Series (Daily)" not in data:
            print(f"AlphaVantage returned no data for {ticker}")
            return None

        ts = data["Time Series (Daily)"]
        df = pd.DataFrame.from_dict(ts, orient="index")
        df.index = pd.to_datetime(df.index)
        df = df.rename(columns={"5. adjusted close": "Close"})
        df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
        df = df.dropna(subset=["Close"])

        print(f"AlphaVantage fallback: loaded {ticker} from AlphaVantage.")
        return df.sort_index()

    except Exception as e:
        print(f"AlphaVantage error for {ticker}: {e}")
        return None
