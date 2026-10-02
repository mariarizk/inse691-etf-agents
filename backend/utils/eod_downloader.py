import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
from backend.utils.fmp_downloader import safe_fmp_download
from backend.utils.csv_downloader import safe_csv_download
from backend.utils.yahoo_downloader import safe_yahoo_download
from backend.utils.alpha_downloader import safe_alpha_download

def fallback_to_fmp(ticker):
    df = safe_fmp_download(ticker)
    if df is not None:
        return df

    print(f"FMP failed for {ticker}, switching to AlphaVantage fallback.")
    df = safe_alpha_download(ticker)
    if df is not None:
        return df

    print(f"AlphaVantage fallback also failed for {ticker}, switching to CSV fallback.")
    df = safe_csv_download(ticker)
    if df is not None:
        return df

    print(f"CSV fallback also failed for {ticker}, returning empty DataFrame.")
    return pd.DataFrame(columns=["Close"])

def safe_eod_download(ticker, period="1y"):
    api_key = os.getenv("EODHD_API_KEY")
    if not api_key:
        print("Missing EODHD_API_KEY")
        return fallback_to_fmp(ticker)

    url = (
        f"https://eodhd.com/api/eod/{ticker}.US?"
        f"period={period}&api_token={api_key}&fmt=json"
    )

    try:
        response = requests.get(url, timeout=10)

        # Debug
        print("\n--- EODHD DEBUG ---")
        print("URL:", url)
        print("Status:", response.status_code)
        print("Raw body:", response.text[:300])
        print("--- END DEBUG ---\n")

        # If daily limit reached → fallback
        if response.status_code == 402:
            print(f"EODHD daily limit reached for {ticker}, switching to FMP.")
            return fallback_to_fmp(ticker)

        # Parse JSON
        data = response.json()

        if not isinstance(data, list) or len(data) == 0:
            print(f"EODHD returned no data for {ticker}, switching to FMP.")
            return fallback_to_fmp(ticker)

        df = pd.DataFrame(data)

        if "date" not in df.columns:
            print(f"EODHD missing 'date' for {ticker}, switching to FMP.")
            return fallback_to_fmp(ticker)

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

        # Standardize for CSV fallback
        df = df.rename(columns={"date": "Date"})
        df["Date"] = df.index
        df = df[["Date", "Close"]]

        # Save CSV fallback
        df.to_csv(f"data/price_cache/{ticker}.csv", index=False)
        print(f"PriceCache: saved {ticker} to CSV fallback.")

        return df.sort_index()

    except Exception as e:
        print(f"EODHD error for {ticker}: {e}, switching to FMP.")
        return fallback_to_fmp(ticker)
