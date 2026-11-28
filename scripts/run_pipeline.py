"""Run one live pipeline analysis on the latest QQQ history + a sample article."""

import os
import sys

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

import pandas as pd

from backend.etf_pipeline import ETFPipeline


def main():
    price_df = pd.read_csv(
        "data/QQQ.csv",
        parse_dates=["Date"],
        index_col="Date",
    )

    article = (
        "Microsoft reported stronger-than-expected earnings and raised "
        "guidance for next quarter. Analysts remain optimistic about "
        "continued growth in cloud and AI demand."
    )

    result = ETFPipeline().run(price_df, article)

    print("\n=== Live Pipeline Result ===\n")
    for key, value in result.items():
        print(f"{key}: {value}\n")


if __name__ == "__main__":
    main()
