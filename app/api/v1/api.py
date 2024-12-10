from fastapi import APIRouter

from app.core.config import settings
from .endpoints import health

api_router = APIRouter(prefix=settings.API_V1_STR)

# Health check endpoint
api_router.include_router(health.router, prefix="/health", tags=["health"])
