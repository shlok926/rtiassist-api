from fastapi import Request, HTTPException, Depends
from datetime import datetime, timedelta, timezone
from typing import Dict, List
import asyncio
from dependencies.auth import get_current_user
from models.orm.user import User
import logging

logger = logging.getLogger(__name__)

# IN-MEMORY RATE LIMITER
# IMPORTANT: Suitable for single-instance / development use.
# Distributed production deployments require shared rate-limit storage (e.g., Redis).

# Stores user_id -> list of timestamps
_rate_limits: Dict[str, List[datetime]] = {}
_lock = asyncio.Lock()

async def rate_limit(
    request: Request,
    user: User = Depends(get_current_user),
    max_requests: int = 5,
    window_minutes: int = 1
):
    """
    Limits the number of requests per user for a specific route.
    Usage: Depends(rate_limit)
    """
    global _rate_limits
    import os
    if os.getenv("ENVIRONMENT", "development") == "development" and request.headers.get("X-Enforce-Rate-Limit") != "true":
        return
        
    # We use a composite key for route + user
    route = request.url.path
    key = f"{user.id}:{route}"
    now = datetime.now(timezone.utc)
    window_start = now - timedelta(minutes=window_minutes)
    
    async with _lock:
        if key not in _rate_limits:
            _rate_limits[key] = []
            
        # Clean up old timestamps
        _rate_limits[key] = [t for t in _rate_limits[key] if t > window_start]
        
        if len(_rate_limits[key]) >= max_requests:
            logger.warning(f"Rate limit exceeded for user {user.id} on route {route}")
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded. Try again in {window_minutes} minute(s)."
            )
            
        _rate_limits[key].append(now)

async def rate_limit_expensive(request: Request, user: User = Depends(get_current_user)):
    """Stricter limit for LLM generation operations: 3 per minute."""
    await rate_limit(request, user, max_requests=3, window_minutes=1)
