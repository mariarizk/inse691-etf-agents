"""Print metrics from the latest historic backtest outputs."""

import os
import sys

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from backend.historic_backtest import run_historic_backtest


def main():
    result = run_historic_backtest(save_outputs=True)
    metrics = result["metrics"]

    print("\n=== MAS Strategy Performance Metrics ===\n")
    for key, value in metrics.items():
        print(f"{key}: {value:.4f}")


if __name__ == "__main__":
    main()
