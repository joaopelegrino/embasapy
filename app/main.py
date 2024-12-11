from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import analysis
from app.core.config import settings

app = FastAPI(
    title="EMBASA API",
    description="API para análise de conteúdo",
    version="0.1.0"
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
app.include_router(
    analysis.router,
    prefix="/analysis",
    tags=["analysis"]
)

@app.get("/health")
async def health_check():
    """Endpoint de health check"""
    return {"status": "healthy"}
