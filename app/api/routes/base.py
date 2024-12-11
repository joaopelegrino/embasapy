from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "EMBASA API v0.1.0"} 