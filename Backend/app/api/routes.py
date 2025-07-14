from fastapi import APIRouter, HTTPException
from app.services.news import fetch_newsapi
from app.db.sqlite import get_articles, save_articles, update_article, delete_article, get_all_articles, get_filtered_articles, clear_articles
from pydantic import BaseModel

router = APIRouter()

class ArticleCreate(BaseModel):
    title: str
    content: str
    source: str
    published_at: str

@router.get("/news", description="Fetch the latest news articles from GNews API for multiple topics, replacing existing articles with clusters")
async def get_news(country: str = None, topics: str = None, query: str = None):
    articles = fetch_newsapi(country=country, topics=topics, query=query)
    if not articles:
        raise HTTPException(status_code=404, detail="No articles found from GNews API")
    clear_articles()
    save_articles(articles)
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logging.debug(f"Saved {len(articles)} articles to database")
    return {"articles": articles}

@router.get("/news/stored", description="Fetch stored news articles with optional filtering and pagination, including cluster IDs")
async def get_stored_news(country: str = None, category: str = None, query: str = None, limit: int = 10, offset: int = 0):
    articles = get_filtered_articles(country, category, query)
    if not articles:
        raise HTTPException(status_code=404, detail="No articles found in database")
    return {"articles": articles[offset:offset + limit]}

@router.post("/news", description="Create a new news article")
async def create_news(article: ArticleCreate):
    save_articles([article.dict()])
    return {"message": "Article created"}

@router.put("/news/{id}", description="Update an existing news article by ID. Requires a JSON body with title, content, source, and published_at.")
async def update_news(id: int, article: dict):
    if update_article(id, article):
        return {"message": "Article updated"}
    raise HTTPException(status_code=404, detail="Article not found")

@router.delete("/news/{id}", description="Delete a news article by ID")
async def delete_news(id: int):
    if delete_article(id):
        return {"message": "Article deleted"}
    raise HTTPException(status_code=404, detail="Article not found")