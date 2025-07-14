import requests
from app.db.sqlite import save_articles, clear_articles
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

logging.basicConfig(level=logging.DEBUG)
GNEWS_API_KEY = '4f3bbc3d001a0d6cd2fbcbf6bf81a75c'
DEFAULT_TOPICS = ["technology", "sports", "business"]


def fetch_newsapi(country: str = None, topics: str = None, query: str = None) -> list:
    url = "https://gnews.io/api/v4/top-headlines"
    all_articles = []

    # Parse topics
    selected_topics = [t.strip().lower() for t in (topics or "").split(",") if t.strip()] if topics else DEFAULT_TOPICS
    selected_topics = selected_topics[:3]  # Limit to 3 topics

    params_base = {
        "token": GNEWS_API_KEY,
        "country": country.lower() if country else None,
        "max": 10,
        "lang": "en"
    }
    params_base = {k: v for k, v in params_base.items() if v is not None}

    logging.debug(f"Fetching news for topics: {selected_topics}")
    for topic in selected_topics:
        params = params_base.copy()
        params["category"] = topic
        if query:
            params["q"] = query

        logging.debug(f"Fetching news with params: {params}")
        try:
            response = requests.get(url, params=params, timeout=10)
            logging.debug(f"Response status code: {response.status_code}")
            response.raise_for_status()
            data = response.json()
            if data.get("totalArticles") == 0:
                logging.warning(f"No articles found for topic: {topic}")
                continue
            articles = data.get("articles", [])

            processed_articles = [
                {
                    "title": str(article.get("title", "No title")),
                    "content": str(article.get("description", "No content") or ""),
                    "source": str(article.get("source", {}).get("name", "No source")),
                    "published_at": str(article.get("publishedAt", "1970-01-01T00:00:00Z")),
                    "country": country.lower() if country else "us",
                    "category": topic  # Use the current topic as category
                }
                for article in articles
            ]
            all_articles.extend(processed_articles)
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed for topic {topic}: {e}")
            continue

    # Clustering
    if all_articles:
        vectorizer = TfidfVectorizer(stop_words='english', max_features=500)
        tfidf_matrix = vectorizer.fit_transform([a["content"] for a in all_articles])
        n_clusters = min(5, len(all_articles))  # Adjust clusters based on number of articles
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        kmeans.fit(tfidf_matrix)
        for i, article in enumerate(all_articles):
            article["cluster_id"] = int(kmeans.labels_[i])

    logging.debug(f"Processed {len(all_articles)} articles with clusters: {all_articles[:1]}")
    clear_articles()
    save_articles(all_articles)
    return all_articles


if __name__ == "__main__":
    articles = fetch_newsapi(country="in", topics="technology,sports", query="AI")
    for article in articles:
        print(article)