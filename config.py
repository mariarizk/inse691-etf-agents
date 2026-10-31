import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"
PRICE_FILE = DATA_DIR / "QQQ.csv"
AGENT_LOG_FILE = DATA_DIR / "agent_log.json"
TICKER = "QQQ"

load_dotenv(ROOT_DIR / ".env")

AGENT_CONFIG = {
    "technical": {
        "short_window": 10,
        "long_window": 30,
    },
    "sentiment": {
        "positive_return": 0.01,
        "negative_return": -0.01,
    },
    "risk": {
        "window": 20,
        "low_volatility": 0.01,
        "medium_volatility": 0.02,
    },
}

LLM_CONFIG = {
    "api_key": os.getenv("GEMINI_API_KEY", ""),
    "base_url": os.getenv(
        "LLM_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai"
    ).rstrip("/"),
    "model": os.getenv("LLM_MODEL", "gemini-3.5-flash-lite"),
    "temperature": 0.2,
    "max_output_tokens": 800,
    "timeout_seconds": 60,
    "max_retries": 2,
    "retry_wait_seconds": 10,
    "explanation_max_words": 120,
    "explanation_max_attempts": 2,
    "report_max_words": 250,
}

NEWS_CONFIG = {
    "api_key": os.getenv("MARKETAUX_API_KEY", ""),
    "base_url": "https://api.marketaux.com/v1/news/all",
    "headline_limit": 3,
    "timeout_seconds": 10,
}
