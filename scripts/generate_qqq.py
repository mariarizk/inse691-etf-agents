import pandas as pd
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.price_cache import safe_eod_download

df = safe_eod_download("QQQ")
df.to_csv("data/QQQ.csv", index=True)

print("Generated data/QQQ.csv")
