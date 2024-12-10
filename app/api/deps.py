from typing import AsyncGenerator, Optional

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from jose import jwt
from loguru import logger

from app.core.config import settings
from app.core.security import ALGORITHM, decode_token

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(
    api_key: Optional[str] = Security(api_key_header)
) -> None:
    """Verify API key."""
    if api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )


async def verify_token(
    token: str,
    required_scopes: Optional[list] = None
) -> dict:
    """Verify JWT token and scopes."""
    try:
        payload = decode_token(token)
        token_scopes = payload.get("scopes", [])
        
        if required_scopes:
            for scope in required_scopes:
                if scope not in token_scopes:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Missing required scope: {scope}",
                    )
        
        return payload
    except Exception as e:
        logger.error(f"Token verification failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
