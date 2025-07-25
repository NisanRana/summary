import sqlite3
import logging

logging.basicConfig(level=logging.DEBUG)

def init_db():
    conn = sqlite3.connect("articles.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS articles
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT,
                  content TEXT,
                  source TEXT,
                  published_at TEXT,
                  country TEXT,
                  category TEXT,
                  cluster_id INTEGER)''')
    conn.commit()
    conn.close()

def clear_articles():
    logging.debug("Clearing all articles from the database")
    conn = sqlite3.connect("articles.db")
    c = conn.cursor()
    c.execute("DELETE FROM articles")
    conn.commit()
    logging.debug("Articles cleared successfully")
    conn.close()

def get_articles(limit: int = 10, offset: int = 0):
    conn = sqlite3.connect("articles.db")
    c = conn.cursor()
    c.execute("SELECT id, title, content, source, published_at FROM articles LIMIT ? OFFSET ?", (limit, offset))
    rows = c.fetchall()
    conn.close()
    return [{"id": row[0], "title": row[1], "content": row[2], "source": row[3], "published_at": row[4]} for row in rows]

def save_articles(articles):
    logging.debug(f"Saving {len(articles)} articles")
    conn = sqlite3.connect("articles.db")
    c = conn.cursor()
    c.executemany("INSERT INTO articles (title, content, source, published_at, country, category, cluster_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  [(a.get("title"), a.get("content"), a.get("source"), a.get("published_at"), a.get("country", ""), a.get("category", ""), a.get("cluster_id", 0)) for a in articles])
    conn.commit()
    logging.debug("Articles saved successfully")
    conn.close()

def get_all_articles():
    conn = sqlite3.connect("articles.db")
    c = conn.cursor()
    c.execute("SELECT * FROM articles")
    rows = c.fetchall()
    conn.close()
    return [{"id": row[0], "title": row[1], "content": row[2], "source": row[3], "published_at": row[4], "country": row[5], "category": row[6], "cluster_id": row[7]} for row in rows]

def update_article(id: int, article: dict):
    conn = sqlite3.connect("articles.db")
    c = conn.cursor()
    c.execute("UPDATE articles SET title = ?, content = ?, source = ?, published_at = ? WHERE id = ?",
              (article.get("title"), article.get("content"), article.get("source"), article.get("published_at"), id))
    conn.commit()
    affected_rows = c.rowcount
    conn.close()
    return affected_rows > 0

def delete_article(id: int):
    conn = sqlite3.connect("articles.db")
    c = conn.cursor()
    c.execute("DELETE FROM articles WHERE id = ?", (id,))
    conn.commit()
    affected_rows = c.rowcount
    conn.close()
    return affected_rows > 0

def get_filtered_articles(country: str = None, category: str = None, query: str = None) -> list:
    conn = sqlite3.connect("articles.db")
    c = conn.cursor()
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
        conditions.append("title LIKE ? OR content LIKE ?")
        params.extend([f"%{query}%", f"%{query}%"])
    if conditions:
        query_str += " WHERE " + " AND ".join(conditions)
    logging.debug(f"Executing query: {query_str} with params: {params}")
    c.execute(query_str, params)
    rows = c.fetchall()
    conn.close()
    return [{"id": row[0], "title": row[1], "content": row[2], "source": row[3], "published_at": row[4], "country": row[5], "category": row[6], "cluster_id": row[7]} for row in rows]