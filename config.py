CONFIG = {
    "balance_sheet": {
        "current_ratio_min": 1.0,
        "debt_to_equity_max": 2.0
    },

    "income_statement": {
        "revenue_growth_min": 0.0,
        "net_margin_min": 0.05
    },

    "cashflow": {
        "operating_cf_min": 0,
        "free_cf_min": 0
    },

    "valuation": {
        "pe_max": 40,
        "pb_max": 10
    },

    "efficiency": {
        "roe_min": 0.05,
        "roa_min": 0.02
    },

    "risk": {
        "volatility_max": 0.05,
        "max_drawdown_max": 0.30
    },

    "sentiment": {
        "positive_threshold": 0.2,
        "negative_threshold": -0.2
    },

    "diversification": {
        "sector_weight_max": 0.4,
        "leverage_penalty": 2
    }
}
