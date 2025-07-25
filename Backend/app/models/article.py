from pydantic import BaseModel
from datetime import datetime

class Article(BaseModel):
    title: str
    content: str
    source: str
    published_at: str
    country: str | None = None
    category: str | None = None
    cluster_id: int = 0

    def to_dict(self) -> dict:
        """Convert Article to dictionary for database storage."""
        return self.dict(exclude_none=True)