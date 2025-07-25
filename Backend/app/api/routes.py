from fastapi import APIRouter, HTTPException
from app.services.news import fetch_newsapi
from app.services.clustering import cluster_articles
from app.db.sqlite import get_articles, save_articles, clear_articles, get_filtered_articles
from app.models.article import Article
from typing import List, Dict

router = APIRouter(prefix="/news", tags=["news"])

@router.get("/", description="Fetch and cluster the latest news articles from GNews API")
async def get_news(country: str = None, topics: str = None, query: str = None) -> Dict[str, List[Dict]]:
    """Fetch news articles, cluster them, and save to database."""
    articles = fetch_newsapi(country=country, topics=topics, query=query)
    if not articles:
        raise HTTPException(status_code=404, detail="No articles found from GNews API")
    
    articles = cluster_articles(articles)
    clear_articles()
    save_articles(articles)
    return {"articles": articles}

@router.get("/stored", description="Fetch stored news articles with optional filtering and pagination")
async def get_stored_news(country: str = None, category: str = None, query: str = None, limit: int = 10, offset: int = 0) -> Dict[str, List[Dict]]:
    """Retrieve filtered and paginated articles from the database."""
    articles = get_filtered_articles(country, category, query)
    if not articles:
        raise HTTPException(status_code=404, detail="No articles found in database")
    return {"articles": articles[offset:offset + limit]}