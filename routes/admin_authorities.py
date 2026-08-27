from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from models.database import get_db
from models.schemas import (
    AuthorityCreateRequest, AuthorityUpdateRequest,
    AuthorityVerificationRequest, AuthorityUnverificationRequest,
    AuthorityResponse, AuthorityHistoryResponse,
    AuthorityImportRequest, AuthorityImportResponse
)
from dependencies.auth import get_admin_user
from models.orm.user import User
from services import authority_service

router = APIRouter(prefix="/admin/authorities", tags=["Admin Authorities"])

@router.post("", response_model=AuthorityResponse)
def create_authority(
    request: AuthorityCreateRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    return authority_service.admin_create_authority(db, request, admin)

@router.patch("/{authority_id}", response_model=AuthorityResponse)
def update_authority(
    authority_id: str,
    request: AuthorityUpdateRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    return authority_service.admin_update_authority(db, authority_id, request, admin)

@router.post("/{authority_id}/verify", response_model=AuthorityResponse)
def verify_authority(
    authority_id: str,
    request: AuthorityVerificationRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    return authority_service.admin_verify_authority(db, authority_id, request, admin)

@router.post("/{authority_id}/unverify", response_model=AuthorityResponse)
def unverify_authority(
    authority_id: str,
    request: AuthorityUnverificationRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    return authority_service.admin_unverify_authority(db, authority_id, request, admin)

@router.get("/{authority_id}/history", response_model=List[AuthorityHistoryResponse])
def get_authority_history(
    authority_id: str,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    return authority_service.admin_get_authority_history(db, authority_id, admin)

@router.get("/review-queue", response_model=List[AuthorityResponse])
def get_review_queue(
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    return authority_service.admin_get_review_queue(db, admin)

@router.post("/import", response_model=AuthorityImportResponse)
def import_authorities(
    request: AuthorityImportRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    return authority_service.admin_import_authorities(db, request, admin)
