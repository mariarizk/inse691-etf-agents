import pandas as pd
import os

def safe_csv_download(ticker):
    path = f"data/price_cache/{ticker}.csv"

    if not os.path.exists(path):
        print(f"CSV fallback: {path} not found.")
        return None

    try:
        df = pd.read_csv(path)

        # Ensure required columns exist
        if "Date" not in df.columns or "Close" not in df.columns:
            print(f"CSV fallback: {ticker}.csv missing required columns.")
            return None

        # Parse dates
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"])
        df = df.set_index("Date")

        # Force numeric Close values
        df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

        # Drop rows where Close is NaN (invalid)
        df = df.dropna(subset=["Close"])

        if df.empty:
            print(f"CSV fallback: {ticker}.csv contains no valid numeric data.")
            return None

        print(f"CSV fallback: loaded sanitized {ticker} from local file.")
        return df.sort_index()

    except Exception as e:
        print(f"CSV fallback error for {ticker}: {e}")
        return None
