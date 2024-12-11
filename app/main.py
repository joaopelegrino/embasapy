from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes import base_router, analysis_router

app = FastAPI(
    title="EMBASA API",
    description="API para análise de conteúdo",
    version="0.1.0",
    docs_url=None if settings.APP_ENV == "production" else "/docs",
    redoc_url=None if settings.APP_ENV == "production" else "/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(base_router)
app.include_router(analysis_router)

@app.get("/health")
async def health_check():
    """Endpoint de health check"""
    return {"status": "healthy"}
