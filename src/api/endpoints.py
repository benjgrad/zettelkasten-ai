from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
from src.services import rss_service

router = APIRouter()

class HealthResponse(BaseModel):
    status: str

class ManualIngestRequest(BaseModel):
    url: str
    content: str = None

class RSSIngestResponse(BaseModel):
    message: str
    results: List[Dict[str, Any]]
    total_feeds_processed: int

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(status="ok")

@router.post("/ingest/manual")
async def manual_ingest(request: ManualIngestRequest):
    """Manual content ingestion endpoint stub"""
    return {
        "message": "Manual ingest endpoint placeholder",
        "url": request.url,
        "status": "received"
    }

@router.post("/ingest/rss", response_model=RSSIngestResponse)
async def rss_ingest():
    """RSS feed ingestion endpoint"""
    try:
        results = rss_service.ingest_all_feeds()

        total_articles = sum(r.get("articles_added", 0) for r in results)

        return RSSIngestResponse(
            message=f"Successfully processed {len(results)} RSS feeds, added {total_articles} new articles",
            results=results,
            total_feeds_processed=len(results)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RSS ingestion failed: {str(e)}")