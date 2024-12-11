from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

from app.core.config import settings

api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Security(api_key_header)):
    """Verifica API key"""
    if api_key != settings.API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Could not validate API key"
        )
    return api_key

router = APIRouter()

@router.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "app": "EMBASA API",
        "version": "0.1.0",
        "status": "running"
    } 