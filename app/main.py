from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import base
from app.core.security import get_api_key

app = FastAPI(
    title="EMBASA API",
    description="API para processamento de dados da EMBASA",
    version="0.1.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas base
app.include_router(base.router, prefix="/api/v1", dependencies=[Depends(get_api_key)])

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "detail": exc.detail,
        "status_code": exc.status_code
    }
