from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from models.database import get_db
from models.schemas import (
    AuthorityCreateRequest, AuthorityUpdateRequest,
    AuthorityVerificationRequest, AuthorityUnverificationRequest,
    AuthorityResponse, AuthorityHistoryResponse,
    AuthorityImportRequest, AuthorityImportResponse,
    OfficialAuthoritySourceResponse, SourceDecisionRequest,
    ProposedAuthorityChangeResponse, ProposedAuthorityChangeReviewRequest
)
from services.source_intelligence import SourceIntelligence
from models.orm.source_registry import OfficialAuthoritySource, ProposedAuthorityChange
from models.orm.authority import Authority, AuthorityVerificationHistory
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

# --- Source Intelligence (Phase 17) ---

@router.post("/sources/trigger-fetch/{source_id}", response_model=OfficialAuthoritySourceResponse)
async def trigger_source_fetch(
    source_id: str,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    source = await SourceIntelligence.check_source(db, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
        
    diff = None
    if source.review_status == "POTENTIAL_CHANGE_REQUIRES_REVIEW":
        diff = SourceIntelligence.generate_diff(
            source.previous_extracted_text or "",
            source.last_extracted_text or ""
        )
        
    # We must construct a dictionary or schema because SQLAlchemy objects don't naturally have diff_summary
    response_data = {
        "id": source.id,
        "authority_id": source.authority_id,
        "source_url": source.source_url,
        "source_type": source.source_type,
        "is_active": source.is_active,
        "last_fetch_status": source.last_fetch_status,
        "last_fetch_error": source.last_fetch_error,
        "last_successful_fetch_at": source.last_successful_fetch_at,
        "last_checked_at": source.last_checked_at,
        "last_parse_status": source.last_parse_status,
        "last_content_hash": source.last_content_hash,
        "last_extracted_text": source.last_extracted_text,
        "previous_extracted_text": source.previous_extracted_text,
        "review_status": source.review_status,
        "diff_summary": diff
    }
    return response_data

@router.post("/sources/{source_id}/review", response_model=OfficialAuthoritySourceResponse)
def review_source_change(
    source_id: str,
    request: SourceDecisionRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    try:
        return SourceIntelligence.review_and_decide(
            db=db,
            source_id=source_id,
            admin_email=admin.email,
            decision=request.decision,
            notes=request.notes
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/sources/{source_id}/proposed-changes", response_model=List[ProposedAuthorityChangeResponse])
def get_proposed_changes(
    source_id: str,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    changes = db.query(ProposedAuthorityChange).filter(
        ProposedAuthorityChange.source_id == source_id,
        ProposedAuthorityChange.review_status == "PENDING_REVIEW"
    ).all()
    return changes

@router.post("/source-changes/{change_id}/review", response_model=ProposedAuthorityChangeResponse)
def review_proposed_change(
    change_id: str,
    request: ProposedAuthorityChangeReviewRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    change = db.query(ProposedAuthorityChange).filter(ProposedAuthorityChange.id == change_id).first()
    if not change:
        raise HTTPException(status_code=404, detail="Change not found")
        
    if change.review_status != "PENDING_REVIEW":
        raise HTTPException(status_code=400, detail=f"Change is already {change.review_status}")
        
    if request.decision not in ["ACCEPT", "REJECT", "MARK_AMBIGUOUS"]:
        raise HTTPException(status_code=400, detail="Invalid decision")
        
    change.review_status = request.decision
    change.reviewed_by = admin.email
    from datetime import datetime, timezone
    change.reviewed_at = datetime.now(timezone.utc)
    change.review_notes = request.notes
    
    if request.decision == "ACCEPT":
        authority = db.query(Authority).filter(Authority.id == change.authority_id).first()
        if not authority:
            raise HTTPException(status_code=404, detail="Authority not found")
            
        # Stale Check: Ensure the trusted Authority value hasn't changed since detection
        current_val = str(getattr(authority, change.field_name, None) or "None")
        expected_old = str(change.old_value or "None")
        if current_val != expected_old:
            raise HTTPException(status_code=400, detail="Stale proposal: The authority field was modified after this proposal was created. Please reject this and fetch again.")
            
        # Update Authority Field safely
        setattr(authority, change.field_name, change.proposed_value)
        
        # We do NOT falsely upgrade the entire Authority to VERIFIED just because one field was accepted.
        # The existing verification status is preserved.
        history = AuthorityVerificationHistory(
            authority_id=authority.id,
            source_url=change.source.source_url,
            source_type=change.source.source_type,
            verification_status=authority.verification_status, # Preserve current status
            verified_by=admin.email,
            notes=f"Accepted extraction for {change.field_name}: {change.old_value} -> {change.proposed_value}. {request.notes or ''}"
        )
        db.add(history)
        authority.last_verified = datetime.now(timezone.utc)
        # We don't overwrite verified_by here unless we want to, but history handles it.
        
    elif request.decision == "MARK_AMBIGUOUS":
        # Keep Authority fail-closed where appropriate
        authority = db.query(Authority).filter(Authority.id == change.authority_id).first()
        if authority and authority.verification_status == "VERIFIED":
            authority.verification_status = "NEEDS_REVIEW"
            history = AuthorityVerificationHistory(
                authority_id=authority.id,
                source_url=change.source.source_url,
                source_type=change.source.source_type,
                verification_status="NEEDS_REVIEW",
                verified_by=admin.email,
                notes=f"Extraction marked ambiguous for {change.field_name}. {request.notes or ''}"
            )
            db.add(history)
            
    db.commit()
    db.refresh(change)
    return change

@router.post("/{authority_id}/sources", response_model=OfficialAuthoritySourceResponse)
def register_official_source(
    authority_id: str,
    source_url: str = Query(...),
    source_type: str = Query(...),
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    authority = authority_service.authority_repository.get_by_id(db, authority_id)
    if not authority:
        raise HTTPException(status_code=404, detail="AUTHORITY_NOT_FOUND")
        
    source = OfficialAuthoritySource(
        authority_id=authority_id,
        source_url=source_url,
        source_type=source_type
    )
    db.add(source)
    db.commit()
    db.refresh(source)
    return source
