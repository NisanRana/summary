# test/test_news.py
from app.services.news import fetch_newsapi
from app.db.sqlite import get_articles, update_article, delete_article, get_all_articles
import sqlite3
import pytest

@pytest.fixture
def setup_article():
    conn = sqlite3.connect("articles.db")
    c = conn.cursor()
    c.execute("INSERT INTO articles (title, content, source, published_at) VALUES (?, ?, ?, ?)",
              ("Test Article", "Original", "UnitTest", "2025-06-12"))
    conn.commit()
    c.execute("SELECT last_insert_rowid()")
    article_id = c.fetchone()[0]
    conn.close()
    yield article_id
    # Cleanup
    conn = sqlite3.connect("articles.db")
    c = conn.cursor()
    c.execute("DELETE FROM articles WHERE id = ?", (article_id,))
    conn.commit()
    conn.close()

# Remove this duplicate
# @pytest.fixture
# def setup_article():
#     insert_test_article()
#     yield
#     delete_article("Test Article")

# --- Utility function (optional, can be kept or removed) ---
def insert_test_article(title="Test Article", content="Original", source="UnitTest", published_at="2025-06-12"):
    conn = sqlite3.connect("articles.db")
    c = conn.cursor()
    c.execute("INSERT INTO articles (title, content, source, published_at) VALUES (?, ?, ?, ?)",
              (title, content, source, published_at))
    conn.commit()
    conn.close()

# --- Test 1: News API fetch ---
def test_fetch_newsapi():
    articles = fetch_newsapi(country="us")
    assert len(articles) > 0
    assert len(get_all_articles()) > 0

# --- Test 2: Get articles from DB ---
def test_get_stored_news():
    result = get_articles()
    assert isinstance(result, list), "Expected a list of articles"
    assert len(result) > 0, "Expected at least one article"

# --- Test 3: Update article ---
def test_update_article(setup_article):
    article_id = setup_article
    print(f"Article ID: {article_id}")  # Debug
    updated_article = {"title": "Updated Title", "content": "Updated Content", "source": "Updated Source", "published_at": "2025-06-26T00:00:00Z"}
    updated = update_article(article_id, updated_article)
    assert updated is True
    conn = sqlite3.connect("articles.db")
    c = conn.cursor()
    c.execute("SELECT title FROM articles WHERE id = ?", (article_id,))
    result = c.fetchone()[0]
    conn.close()
    assert result == "Updated Title"

# --- Test 4: Delete article (uncomment and fix) ---
def test_delete_article(setup_article):
    article_id = setup_article
    print(f"Article ID: {article_id}")  # Debug
    deleted = delete_article(article_id)
    assert deleted is True
    conn = sqlite3.connect("articles.db")
    c = conn.cursor()
    c.execute("SELECT id FROM articles WHERE id = ?", (article_id,))
    result = c.fetchone()
    conn.close()
    assert result is None

# --- Test 5: Filtering ---
def test_filtering():
    articles = get_all_articles()
    filtered = [a for a in articles if "tech" in a.get("content", "").lower()]
    assert len(filtered) <= len(articles)