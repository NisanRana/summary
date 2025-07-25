import requests
import logging
from typing import List, Dict
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")
DEFAULT_TOPICS = ["technology", "sports", "business"]

def fetch_newsapi(country: str = None, topics: str = None, query: str = None) -> List[Dict]:
    """Fetch news articles from GNews API for specified topics and country."""
    url = "https://gnews.io/api/v4/top-headlines"
    all_articles = []

    selected_topics = [t.strip().lower() for t in (topics or "").split(",") if t.strip()] or DEFAULT_TOPICS
    selected_topics = selected_topics[:3]  # Limit to 3 topics

    params_base = {
        "token": GNEWS_API_KEY,
        "max": 10,
        "lang": "en",
        **({"country": country.lower()} if country else {})
    }

    logger.info(f"Fetching news for topics: {selected_topics}")
    for topic in selected_topics:
        params = params_base.copy()
        params["category"] = topic
        if query:
            params["q"] = query

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            articles = data.get("articles", [])
            if not articles:
                logger.warning(f"No articles found for topic: {topic}")
                continue

            processed_articles = [
                {
                    "title": str(article.get("title", "No title")),
                    "content": str(article.get("description", "No content") or ""),
                    "source": str(article.get("source", {}).get("name", "No source")),
                    "published_at": str(article.get("publishedAt", "1970-01-01T00:00:00Z")),
                    "country": country.lower() if country else "us",
                    "category": topic
                }
                for article in articles
                if article.get("description")  # Ensure content is not empty
            ]
            all_articles.extend(processed_articles)
        except requests.RequestException as e:
            logger.error(f"Failed to fetch news for topic {topic}: {e}")
            continue

    logger.info(f"Fetched {len(all_articles)} articles")
    return all_articles

if __name__ == "__main__":
    articles = fetch_newsapi(country="in", topics="technology,sports", query="AI")
    for article in articles:
        print(article)