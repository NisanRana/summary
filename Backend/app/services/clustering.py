import logging
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

logger = logging.getLogger(__name__)

def cluster_articles(articles: List[Dict]) -> List[Dict]:
    """Cluster articles based on content using TF-IDF and KMeans."""
    if not articles:
        logger.warning("No articles to cluster")
        return articles

    try:
        # Filter out articles with empty content
        valid_articles = [a for a in articles if a.get("content")]
        if not valid_articles:
            logger.warning("No valid articles with content for clustering")
            return articles

        # Vectorize content
        vectorizer = TfidfVectorizer(stop_words="english", max_features=300)
        tfidf_matrix = vectorizer.fit_transform([a["content"] for a in valid_articles])

        # Cluster
        n_clusters = min(5, len(valid_articles))
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        kmeans.fit(tfidf_matrix)

        # Assign cluster IDs
        for i, article in enumerate(valid_articles):
            article["cluster_id"] = int(kmeans.labels_[i])

        # Assign cluster_id=0 to articles with no content
        for article in articles:
            if "cluster_id" not in article:
                article["cluster_id"] = 0

        logger.info(f"Clustered {len(valid_articles)} articles into {n_clusters} clusters")
        return articles
    except Exception as e:
        logger.error(f"Clustering failed: {e}")
        return [dict(a, cluster_id=0) for a in articles]