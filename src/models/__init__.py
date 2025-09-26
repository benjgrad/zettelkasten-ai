import sqlite3
import os
from datetime import datetime
from typing import Optional, List, Dict, Any

class DatabaseManager:
    def __init__(self, db_path: str = "database.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS feeds (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    url TEXT NOT NULL UNIQUE,
                    last_fetched TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    feed_id INTEGER,
                    title TEXT NOT NULL,
                    url TEXT NOT NULL UNIQUE,
                    content TEXT,
                    summary TEXT,
                    published TIMESTAMP,
                    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (feed_id) REFERENCES feeds (id)
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS entities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    article_id INTEGER,
                    text TEXT NOT NULL,
                    label TEXT NOT NULL,
                    start_pos INTEGER,
                    end_pos INTEGER,
                    confidence REAL DEFAULT 1.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (article_id) REFERENCES articles (id)
                )
            """)
            conn.commit()

    def add_feed(self, name: str, url: str) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "INSERT OR IGNORE INTO feeds (name, url) VALUES (?, ?)",
                (name, url)
            )
            conn.commit()
            return cursor.lastrowid or self.get_feed_by_url(url)["id"]

    def get_feed_by_url(self, url: str) -> Optional[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM feeds WHERE url = ?", (url,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def add_article(self, feed_id: int, title: str, url: str, content: str = None,
                   summary: str = None, published: datetime = None) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """INSERT OR IGNORE INTO articles
                   (feed_id, title, url, content, summary, published)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (feed_id, title, url, content, summary, published)
            )
            conn.commit()
            return cursor.lastrowid

    def get_articles_count(self) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM articles")
            return cursor.fetchone()[0]

    def update_feed_last_fetched(self, feed_id: int):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE feeds SET last_fetched = CURRENT_TIMESTAMP WHERE id = ?",
                (feed_id,)
            )
            conn.commit()

    def add_entity(self, article_id: int, text: str, label: str,
                   start_pos: int, end_pos: int, confidence: float = 1.0) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """INSERT INTO entities
                   (article_id, text, label, start_pos, end_pos, confidence)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (article_id, text, label, start_pos, end_pos, confidence)
            )
            conn.commit()
            return cursor.lastrowid

    def get_entities_by_article(self, article_id: int) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM entities WHERE article_id = ? ORDER BY start_pos",
                (article_id,)
            )
            return [dict(row) for row in cursor.fetchall()]

    def get_connection(self):
        return sqlite3.connect(self.db_path)

db = DatabaseManager()