import os
import sys
import unittest

import pandas as pd

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from backend.etf_pipeline import ETFPipeline
from backend.historic_backtest import run_historic_backtest


class TestFullSystem(unittest.TestCase):

    def test_live_pipeline_plus_historic_backtest(self):
        price_df = pd.read_csv(
            "data/QQQ.csv",
            parse_dates=["Date"],
            index_col="Date",
        )
        article = (
            "Microsoft reported stronger-than-expected earnings "
            "and raised guidance for next quarter."
        )

        live = ETFPipeline().run(price_df, article)
        self.assertIn(live["decision"]["action"], [-1, 0, 1])

        historic = run_historic_backtest(
            price_csv="data/QQQ.csv",
            save_outputs=False,
        )
        self.assertIn("equity_curve", historic["backtest"])
        self.assertEqual(
            len(historic["decisions"]),
            len(historic["price_df"]),
        )


if __name__ == "__main__":
    unittest.main()
