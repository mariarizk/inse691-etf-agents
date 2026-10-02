import yfinance as yf
import pandas as pd

def safe_yahoo_download(ticker):
    try:
        df = yf.download(ticker, period="max")

        if df is None or df.empty:
            print(f"Yahoo returned no data for {ticker}")
            return None

        # Standardize format
        df = df.rename(columns={"Close": "Close"})
        df = df[["Close"]].copy()

        # Ensure datetime index
        df.index = pd.to_datetime(df.index)

        print(f"Yahoo fallback: loaded {ticker} from Yahoo Finance.")
        return df

    except Exception as e:
        print(f"Yahoo error for {ticker}: {e}")
        return None
