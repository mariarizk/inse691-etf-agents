import requests

from config import NEWS_CONFIG


def fetch_headlines(ticker, limit=None, settings=None):
    """Latest English news for a ticker from Marketaux. Returns [] on any failure."""
    settings = settings or NEWS_CONFIG
    if not settings["api_key"]:
        print("Missing MARKETAUX_API_KEY")
        return []

    params = {
        "symbols": ticker,
        "filter_entities": "true",
        "language": "en",
        "limit": limit or settings["headline_limit"],
        "api_token": settings["api_key"],
    }

    try:
        response = requests.get(settings["base_url"], params=params, timeout=settings["timeout_seconds"])
        response.raise_for_status()
        body = response.json()
    except (requests.RequestException, ValueError) as exc:
        print(f"Marketaux error for {ticker}: {exc}")
        return []

    articles = body.get("data", []) if isinstance(body, dict) else []
    return [
        {
            "title": article.get("title") or "",
            "description": article.get("description") or article.get("snippet") or "",
            "source": article.get("source") or "",
            "published_at": article.get("published_at") or "",
        }
        for article in articles
        if isinstance(article, dict)
    ]


def headlines_to_text(headlines):
    """Joins headlines into one article text for the sentiment and risk agents."""
    return "\n\n".join(
        f"{h['title']}. {h['description']} ({h['source']}, {h['published_at']})".strip()
        for h in headlines
    )
