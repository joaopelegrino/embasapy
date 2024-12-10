from fastapi import APIRouter, Depends
from loguru import logger

from app.api.deps import verify_api_key

router = APIRouter()


@router.get("/", dependencies=[Depends(verify_api_key)])
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: Status information about the API
    """
    logger.info("Health check requested")
    return {
        "status": "healthy",
        "message": "API is running"
    } 