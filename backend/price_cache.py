# backend/price_cache.py

import os
import pandas as pd
from backend.utils.eod_downloader import safe_eod_download

class PriceCache:
    def __init__(self):
        self.cache = {}

    def _path(self, ticker):
        return os.path.join(self.cache_dir, f"{ticker}.csv")

    def get(self, ticker, start, end):
        # Ensure cache exists
        if not hasattr(self, "cache"):
            self.cache = {}

        # Return cached data if available
        if ticker in self.cache:
            return self.cache[ticker]

        # Download data (EODHD → fallback to FMP → fallback to CSV)
        df = safe_eod_download(ticker)

        # If df is None or empty, return empty DataFrame immediately
        if df is None or df.empty:
            print(f"PriceCache: No usable data for {ticker}, returning empty DataFrame.")
            empty = pd.DataFrame(columns=["Close"])
            self.cache[ticker] = empty
            return empty

        # Ensure index is datetime
        if not isinstance(df.index, pd.DatetimeIndex):
            try:
                df.index = pd.to_datetime(df.index)
            except Exception:
                print(f"PriceCache: Could not convert index to datetime for {ticker}.")
                empty = pd.DataFrame(columns=["Close"])
                self.cache[ticker] = empty
                return empty

        # Filter by date
        df = df[(df.index >= pd.to_datetime(start)) & (df.index <= pd.to_datetime(end))]

        # If filtering removes everything, return empty DataFrame
        if df.empty:
            print(f"PriceCache: Filtered data empty for {ticker}.")
            empty = pd.DataFrame(columns=["Close"])
            self.cache[ticker] = empty
            return empty

        # Ensure Close column exists
        if "Close" not in df.columns:
            print(f"PriceCache: Close column missing for {ticker}.")
            empty = pd.DataFrame(columns=["Close"])
            self.cache[ticker] = empty
            return empty

        # Sanitize Close column
        df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
        df = df.dropna(subset=["Close"])

        if df.empty:
            print(f"PriceCache: Sanitized data empty for {ticker}.")
            empty = pd.DataFrame(columns=["Close"])
            self.cache[ticker] = empty
            return empty

        # Save sanitized data to CSV for future fallback
        save_path = f"data/price_cache/{ticker}.csv"
        try:
            df.to_csv(save_path)
            print(f"PriceCache: saved {ticker} to CSV fallback.")
        except Exception as e:
            print(f"PriceCache: Could not save CSV for {ticker}: {e}")

        # Finalize
        df = df[["Close"]].copy()
        self.cache[ticker] = df
        return df
