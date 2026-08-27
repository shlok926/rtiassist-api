from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from models.database import get_db
from models.schemas import AuthoritySearchResponse
from services import authority_service
from typing import Optional

router = APIRouter(prefix="/authorities", tags=["Authorities"])

@router.get("/search", response_model=AuthoritySearchResponse)
def search_authorities(
    department: Optional[str] = None,
    ministry: Optional[str] = None,
    government_level: Optional[str] = None,
    state: Optional[str] = None,
    district: Optional[str] = None,
    verification_status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Search for verified authorities based on criteria."""
    results = authority_service.search_authorities(
        db, department, ministry, government_level, state, district, verification_status
    )
    return AuthoritySearchResponse(results=results)
