from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
from src.services import rss_service, entity_service, vector_storage, diagram_generator

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

class EntityExtractionRequest(BaseModel):
    article_id: int

class EntityExtractionResponse(BaseModel):
    message: str
    result: Dict[str, Any]

class SemanticSearchRequest(BaseModel):
    query: str
    limit: int = 10

class SemanticSearchResponse(BaseModel):
    message: str
    result: Dict[str, Any]

class BatchEmbeddingResponse(BaseModel):
    message: str
    result: Dict[str, Any]

class DiagramGenerationRequest(BaseModel):
    article_id: int

class DiagramGenerationResponse(BaseModel):
    message: str
    result: Dict[str, Any]

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

@router.post("/entities/extract", response_model=EntityExtractionResponse)
async def extract_entities(request: EntityExtractionRequest):
    """Extract entities from a specific article"""
    try:
        result = entity_service.process_article(request.article_id)

        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])

        return EntityExtractionResponse(
            message=f"Extracted {result['entities_found']} entities from article {request.article_id}",
            result=result
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Entity extraction failed: {str(e)}")

@router.post("/search/semantic", response_model=SemanticSearchResponse)
async def semantic_search(request: SemanticSearchRequest):
    """Perform semantic search on articles"""
    try:
        result = vector_storage.semantic_search(request.query, request.limit)

        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])

        return SemanticSearchResponse(
            message=f"Found {result['results_count']} results for query: '{request.query}'",
            result=result
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Semantic search failed: {str(e)}")

@router.post("/embeddings/batch", response_model=BatchEmbeddingResponse)
async def batch_create_embeddings():
    """Create embeddings for all articles"""
    try:
        result = vector_storage.batch_add_embeddings()

        return BatchEmbeddingResponse(
            message=f"Processed {result['total_articles']} articles: {result['successful']} successful, {result['failed']} failed",
            result=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch embedding creation failed: {str(e)}")

@router.get("/embeddings/stats")
async def get_embedding_stats():
    """Get vector storage statistics"""
    try:
        stats = vector_storage.get_collection_stats()
        return {"message": "Vector storage statistics", "result": stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")

@router.post("/diagrams/generate", response_model=DiagramGenerationResponse)
async def generate_diagram(request: DiagramGenerationRequest):
    """Generate MermaidJS diagram from article entities"""
    try:
        result = diagram_generator.generate_diagram_from_article(request.article_id)

        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])

        return DiagramGenerationResponse(
            message=f"Generated MermaidJS diagram for article {request.article_id} with {result['entities_count']} entities",
            result=result
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Diagram generation failed: {str(e)}")