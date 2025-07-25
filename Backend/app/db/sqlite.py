import sqlite3
import logging
from typing import List, Dict
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///articles.db")

def init_db():
    """Initialize the SQLite database and create the articles table."""
    with sqlite3.connect(DATABASE_URL.replace("sqlite:///", "")) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content TEXT,
                source TEXT,
                published_at TEXT,
                country TEXT,
                category TEXT,
                cluster_id INTEGER
            )
        ''')
        conn.commit()

def clear_articles():
    """Clear all articles from the database."""
    with sqlite3.connect(DATABASE_URL.replace("sqlite:///", "")) as conn:
        conn.execute("DELETE FROM articles")
        conn.commit()
        logger.info("All articles cleared from database")

def get_articles(limit: int = 10, offset: int = 0) -> List[Dict]:
    """Retrieve paginated articles from the database."""
    with sqlite3.connect(DATABASE_URL.replace("sqlite:///", "")) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, title, content, source, published_at, country, category, cluster_id "
            "FROM articles LIMIT ? OFFSET ?",
            (limit, offset)
        )
        return [dict(row) for row in cursor.fetchall()]

def save_articles(articles: List[Dict]):
    """Save a list of articles to the database."""
    if not articles:
        logger.warning("No articles to save")
        return

    with sqlite3.connect(DATABASE_URL.replace("sqlite:///", "")) as conn:
        conn.executemany(
            "INSERT INTO articles (title, content, source, published_at, country, category, cluster_id) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            [(a.get("title"), a.get("content"), a.get("source"), a.get("published_at"),
              a.get("country", ""), a.get("category", ""), a.get("cluster_id", 0))
             for a in articles]
        )
        conn.commit()
        logger.info(f"Saved {len(articles)} articles to database")

def get_filtered_articles(country: str = None, category: str = None, query: str = None) -> List[Dict]:
    """Retrieve filtered articles from the database."""
    with sqlite3.connect(DATABASE_URL.replace("sqlite:///", "")) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        query_str = "SELECT id, title, content, source, published_at, country, category, cluster_id FROM articles"
        params = []
        conditions = []

        if country:
            conditions.append("country = ?")
            params.append(country.lower())
        if category:
            conditions.append("category = ?")
            params.append(category.lower())
        if query:
            conditions.append("(title LIKE ? OR content LIKE ?)")
            params.extend([f"%{query}%", f"%{query}%"])

        if conditions:
            query_str += " WHERE " + " AND ".join(conditions)

        logger.debug(f"Executing query: {query_str} with params: {params}")
        cursor.execute(query_str, params)
        return [dict(row) for row in cursor.fetchall()]