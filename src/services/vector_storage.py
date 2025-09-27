import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional
import os
import sqlite3
from src.models import db

class VectorStorageService:
    def __init__(self, chroma_db_path: str = "./chroma_db"):
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=chroma_db_path)

        # Initialize sentence transformer model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

        # Get or create the articles collection
        self.collection = self.client.get_or_create_collection(
            name="articles",
            metadata={"description": "Article embeddings for semantic search"}
        )

    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for given text"""
        embedding = self.embedding_model.encode(text)
        return embedding.tolist()

    def add_article_embedding(self, article_id: int) -> Dict[str, Any]:
        """Add or update embedding for an article"""
        # Get article from database
        with db.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT id, title, content, summary FROM articles WHERE id = ?",
                (article_id,)
            )
            article = cursor.fetchone()

        if not article:
            return {"error": f"Article {article_id} not found"}

        # Create text for embedding (title + summary/content)
        title = article["title"] or ""
        content = article["content"] or article["summary"] or ""

        # Combine title and content for better semantic representation
        text_for_embedding = f"{title}. {content}"

        if not text_for_embedding.strip():
            return {"error": "No text content available for embedding"}

        try:
            # Generate embedding
            embedding = self.generate_embedding(text_for_embedding)

            # Store in ChromaDB
            self.collection.upsert(
                ids=[str(article_id)],
                embeddings=[embedding],
                metadatas=[{
                    "article_id": article_id,
                    "title": title,
                    "text_length": len(text_for_embedding)
                }],
                documents=[text_for_embedding[:1000]]  # Store first 1000 chars as document
            )

            return {
                "article_id": article_id,
                "title": title,
                "text_length": len(text_for_embedding),
                "embedding_dimension": len(embedding),
                "status": "stored"
            }

        except Exception as e:
            return {"error": f"Failed to generate/store embedding: {str(e)}"}

    def semantic_search(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Perform semantic search on stored articles"""
        try:
            # Generate embedding for query
            query_embedding = self.generate_embedding(query)

            # Search in ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=limit,
                include=["metadatas", "documents", "distances"]
            )

            # Format results
            search_results = []
            if results["ids"] and len(results["ids"]) > 0:
                for i, article_id in enumerate(results["ids"][0]):
                    metadata = results["metadatas"][0][i] if results["metadatas"] else {}
                    document = results["documents"][0][i] if results["documents"] else ""
                    distance = results["distances"][0][i] if results["distances"] else 0.0

                    # ChromaDB uses cosine distance, smaller is more similar
                    # Convert to similarity score where higher is better
                    similarity_score = max(0.0, 1.0 - distance) if distance <= 1.0 else 1.0 / (1.0 + distance)

                    search_results.append({
                        "article_id": int(article_id),
                        "title": metadata.get("title", ""),
                        "similarity_score": similarity_score,
                        "distance": distance,
                        "text_preview": document[:200] + "..." if len(document) > 200 else document
                    })

            return {
                "query": query,
                "results_count": len(search_results),
                "results": search_results
            }

        except Exception as e:
            return {"error": f"Search failed: {str(e)}"}

    def batch_add_embeddings(self, article_ids: List[int] = None) -> Dict[str, Any]:
        """Add embeddings for multiple articles"""
        if article_ids is None:
            # Get all articles if no specific IDs provided
            with db.get_connection() as conn:
                cursor = conn.execute("SELECT id FROM articles")
                article_ids = [row[0] for row in cursor.fetchall()]

        results = {
            "total_articles": len(article_ids),
            "successful": 0,
            "failed": 0,
            "errors": []
        }

        for article_id in article_ids:
            result = self.add_article_embedding(article_id)
            if "error" in result:
                results["failed"] += 1
                results["errors"].append(f"Article {article_id}: {result['error']}")
            else:
                results["successful"] += 1

        return results

    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector collection"""
        try:
            count = self.collection.count()
            return {
                "total_embeddings": count,
                "collection_name": self.collection.name,
                "embedding_model": "all-MiniLM-L6-v2",
                "embedding_dimension": 384  # MiniLM-L6-v2 dimension
            }
        except Exception as e:
            return {"error": f"Failed to get stats: {str(e)}"}

vector_storage = VectorStorageService()