import feedparser
import requests
from datetime import datetime
from typing import List, Dict, Any
from src.models import db

class RSSIngestionService:
    DEFAULT_FEEDS = [
        {"name": "Reuters Top News", "url": "https://feeds.reuters.com/reuters/topNews"},
        {"name": "BBC News", "url": "https://feeds.bbci.co.uk/news/rss.xml"},
        {"name": "MIT Technology Review", "url": "https://www.technologyreview.com/feed/"}
    ]

    def __init__(self):
        self.setup_default_feeds()

    def setup_default_feeds(self):
        for feed_info in self.DEFAULT_FEEDS:
            db.add_feed(feed_info["name"], feed_info["url"])

    def fetch_feed(self, feed_url: str) -> Dict[str, Any]:
        try:
            feed = feedparser.parse(feed_url)
            if feed.bozo:
                return {"error": f"Feed parsing error: {feed.bozo_exception}"}

            return {
                "title": getattr(feed.feed, 'title', 'Unknown'),
                "entries": feed.entries,
                "updated": getattr(feed.feed, 'updated', None)
            }
        except Exception as e:
            return {"error": f"Failed to fetch feed: {str(e)}"}

    def process_articles(self, feed_url: str, max_articles: int = 20) -> Dict[str, Any]:
        feed_data = self.fetch_feed(feed_url)

        if "error" in feed_data:
            return feed_data

        feed_info = db.get_feed_by_url(feed_url)
        if not feed_info:
            return {"error": "Feed not found in database"}

        feed_id = feed_info["id"]
        articles_added = 0

        for entry in feed_data["entries"][:max_articles]:
            title = getattr(entry, 'title', 'No title')
            link = getattr(entry, 'link', '')
            summary = getattr(entry, 'summary', '')

            published = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                published = datetime(*entry.published_parsed[:6])

            if db.add_article(feed_id, title, link, summary, summary, published):
                articles_added += 1

        db.update_feed_last_fetched(feed_id)

        return {
            "feed_title": feed_data["title"],
            "articles_processed": len(feed_data["entries"][:max_articles]),
            "articles_added": articles_added,
            "total_articles_in_db": db.get_articles_count()
        }

    def ingest_all_feeds(self) -> List[Dict[str, Any]]:
        results = []
        for feed_info in self.DEFAULT_FEEDS:
            result = self.process_articles(feed_info["url"])
            result["feed_name"] = feed_info["name"]
            results.append(result)
        return results

rss_service = RSSIngestionService()