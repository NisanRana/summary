
class Article:
    def __init__(self, title: str, content: str, source: str, published_at: str):
        self.title = title
        self.content = content
        self.source = source
        self.published_at = published_at

    def to_dict(self):
        return {
            "title": self.title,
            "content": self.content,
            "source": self.source,
            "published_at": self.published_at
        }