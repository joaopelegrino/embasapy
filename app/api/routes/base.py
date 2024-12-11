from fastapi import APIRouter, Depends, HTTPException, Security, Query
from fastapi.security.api_key import APIKeyHeader
from typing import Dict

from app.core.config import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """Verifica API key"""
    if not api_key or api_key != settings.API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Could not validate API key"
        )
    return api_key

router = APIRouter(tags=["base"])

@router.get("/", response_model=Dict[str, str])
async def root():
    """Endpoint raiz"""
    return {
        "app": "EMBASA API",
        "version": "0.1.0",
        "status": "running",
        "env": settings.APP_ENV
    } 