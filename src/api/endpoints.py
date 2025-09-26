from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter()

class HealthResponse(BaseModel):
    status: str

class ManualIngestRequest(BaseModel):
    url: str
    content: str = None

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