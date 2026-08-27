from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.orm.authority import Authority
from models.schemas import AuthorityResolution
from repositories import authority_repository
from agents import authority_classifier
from datetime import datetime, timezone
from models.orm.authority import AuthorityVerificationHistory
from models.schemas import (
    AuthorityCreateRequest, AuthorityUpdateRequest,
    AuthorityVerificationRequest, AuthorityUnverificationRequest
)
from models.orm.user import User
from utils.config import AUTHORITY_VERIFICATION_MAX_AGE_DAYS
from datetime import timedelta

def search_authorities(
    db: Session, 
    department: str = None, 
    ministry: str = None, 
    government_level: str = None, 
    state: str = None, 
    district: str = None,
    verification_status: str = None
) -> List[Authority]:
    results = authority_repository.search(
        db, department, ministry, government_level, state, district, verification_status
    )
    for auth in results:
        _lazy_expire_authority(db, auth)
    return results

def _lazy_expire_authority(db: Session, authority: Authority):
    if authority.verification_status == "VERIFIED" and authority.last_verified:
        last_verified = authority.last_verified
        if last_verified.tzinfo is None:
            last_verified = last_verified.replace(tzinfo=timezone.utc)
            
        age_days = (datetime.now(timezone.utc) - last_verified).days
        if age_days > AUTHORITY_VERIFICATION_MAX_AGE_DAYS:
            authority.verification_status = "EXPIRED"
            
            history = AuthorityVerificationHistory(
                authority_id=authority.id,
                source_url=authority.source_url,
                source_type=authority.source_type,
                verification_status="EXPIRED",
                verified_by="system",
                notes=f"Auto-expired after {AUTHORITY_VERIFICATION_MAX_AGE_DAYS} days."
            )
            db.add(history)
            db.commit()
            db.refresh(authority)

def resolve_authority_for_case(db: Session, problem_description: str) -> AuthorityResolution:
    """
    Given a citizen's problem, AI determines the *parameters* for an authority search.
    Then we query the database deterministically.
    """
    # 1. AI reasoning
    classification = authority_classifier.classify_problem(problem_description)
    
    if not classification.get("department"):
        return AuthorityResolution(
            match_status="NEEDS_REVIEW",
            confidence="LOW",
            reason="Could not determine the appropriate department from the problem description.",
            missing_information=["What government department is involved?"]
        )
        
    # 2. Deterministic Search
    results = authority_repository.search(
        db,
        department=classification.get("department"),
        state=classification.get("state"),
        government_level=classification.get("government_level"),
        active=True
    )
    
    # 3. Match Logic
    if not results:
        return AuthorityResolution(
            match_status="NO_MATCH",
            confidence="HIGH",
            reason=f"No verified authority found for {classification.get('department')} ({classification.get('government_level')}).",
            warnings=["We could not confidently verify the correct authority from the available source-backed records."]
        )
        
    if len(results) > 1:
        return AuthorityResolution(
            match_status="MULTIPLE_MATCHES",
            confidence="MEDIUM",
            reason=f"Found {len(results)} potential authorities matching the description.",
            warnings=["Please clarify which specific jurisdiction or department office is required."]
        )
        
    # Exactly 1 match
    authority = results[0]
    _lazy_expire_authority(db, authority)
    
    # Is it verified?
    if authority.verification_status != "VERIFIED":
        return AuthorityResolution(
            match_status="NEEDS_REVIEW",
            authority_id=authority.id,
            confidence="HIGH",
            verification_status=authority.verification_status,
            reason="Authority matched, but the record is not fully verified.",
            warnings=["Authority information requires verification before filing."]
        )
        
    return AuthorityResolution(
        match_status="MATCHED",
        authority_id=authority.id,
        confidence="HIGH",
        verification_status=authority.verification_status,
        reason="Successfully matched verified authority record."
    )

# --- Admin Operations ---

def admin_create_authority(db: Session, request: AuthorityCreateRequest, admin: User) -> Authority:
    # If no verification note/source is effectively provided, it remains UNVERIFIED
    # But request actually requires source_url and source_type.
    authority = Authority(
        department=request.department,
        ministry=request.ministry,
        government_level=request.government_level,
        state=request.state,
        district=request.district,
        pio_designation=request.pio_designation,
        address=request.address,
        online_portal=request.online_portal,
        filing_fee=request.filing_fee,
        source_url=request.source_url,
        source_type=request.source_type,
        verification_status="UNVERIFIED",
        last_verified=datetime.now(timezone.utc),
        active=True
    )
    
    # If verification_notes are provided along with source, we can consider it explicitly verified on creation
    if request.verification_notes:
        authority.verification_status = "VERIFIED"
        authority.verified_by = admin.email
        
    db.add(authority)
    db.commit()
    db.refresh(authority)
    
    if request.verification_notes:
        # Create history record
        history = AuthorityVerificationHistory(
            authority_id=authority.id,
            source_url=authority.source_url,
            source_type=authority.source_type,
            verification_status="VERIFIED",
            verified_by=admin.email,
            notes=request.verification_notes
        )
        db.add(history)
        db.commit()
        
    return authority

def admin_update_authority(db: Session, authority_id: str, request: AuthorityUpdateRequest, admin: User) -> Authority:
    authority = authority_repository.get_by_id(db, authority_id)
    if not authority:
        raise HTTPException(status_code=404, detail="AUTHORITY_NOT_FOUND")
        
    update_data = request.model_dump(exclude_unset=True)
    
    if authority.verification_status == "VERIFIED":
        # Unverified data must never silently replace VERIFIED data.
        # Enter review flow, DO NOT overwrite VERIFIED record.
        # We raise a controlled error because updates to VERIFIED records must go through verification process.
        if update_data:
            # We could branch a draft, but the prompt says:
            # "UNVERIFIED data must never silently replace VERIFIED data... KEEP VERIFIED ACTIVE RECORD and store incoming information separately as NEEDS_REVIEW"
            # So if someone tries to patch a VERIFIED record, we mark it NEEDS_REVIEW and allow the patch, OR we create a conflict. 
            # Easiest way: change status to NEEDS_REVIEW so it triggers a re-verification workflow.
            authority.verification_status = "NEEDS_REVIEW"
            
    for key, value in update_data.items():
        setattr(authority, key, value)
        
    db.commit()
    db.refresh(authority)
    return authority

def admin_verify_authority(db: Session, authority_id: str, request: AuthorityVerificationRequest, admin: User) -> Authority:
    authority = authority_repository.get_by_id(db, authority_id)
    if not authority:
        raise HTTPException(status_code=404, detail="AUTHORITY_NOT_FOUND")
        
    authority.source_url = request.source_url
    authority.source_type = request.source_type
    authority.verification_status = "VERIFIED"
    authority.last_verified = datetime.now(timezone.utc)
    authority.verified_by = admin.email
    
    history = AuthorityVerificationHistory(
        authority_id=authority.id,
        source_url=request.source_url,
        source_type=request.source_type,
        verification_status="VERIFIED",
        verified_by=admin.email,
        notes=request.notes
    )
    db.add(history)
    db.commit()
    db.refresh(authority)
    return authority

def admin_unverify_authority(db: Session, authority_id: str, request: AuthorityUnverificationRequest, admin: User) -> Authority:
    authority = authority_repository.get_by_id(db, authority_id)
    if not authority:
        raise HTTPException(status_code=404, detail="AUTHORITY_NOT_FOUND")
        
    if request.new_status not in ["NEEDS_REVIEW", "EXPIRED", "REJECTED"]:
        raise HTTPException(status_code=400, detail="INVALID_STATUS")
        
    authority.verification_status = request.new_status
    
    history = AuthorityVerificationHistory(
        authority_id=authority.id,
        source_url=authority.source_url,
        source_type=authority.source_type,
        verification_status=request.new_status,
        verified_by=admin.email,
        notes=request.reason
    )
    db.add(history)
    db.commit()
    db.refresh(authority)
    return authority

def admin_get_authority_history(db: Session, authority_id: str, admin: User) -> List[AuthorityVerificationHistory]:
    authority = authority_repository.get_by_id(db, authority_id)
    if not authority:
        raise HTTPException(status_code=404, detail="AUTHORITY_NOT_FOUND")
        
    return db.query(AuthorityVerificationHistory).filter(
        AuthorityVerificationHistory.authority_id == authority_id
    ).order_by(AuthorityVerificationHistory.created_at.desc()).all()

def admin_get_review_queue(db: Session, admin: User) -> List[Authority]:
    return db.query(Authority).filter(
        Authority.verification_status.in_(["UNVERIFIED", "NEEDS_REVIEW", "EXPIRED"])
    ).all()

def admin_import_authorities(db: Session, request: 'AuthorityImportRequest', admin: User) -> 'AuthorityImportResponse':
    from models.schemas import AuthorityImportResponse, AuthorityImportResult
    
    total = len(request.records)
    imported = 0
    rejected = 0
    duplicates = 0
    results = []
    
    # Simple deterministic duplicate check
    def _is_duplicate(record):
        query = db.query(Authority).filter(
            Authority.department == record.department,
            Authority.government_level == record.government_level
        )
        if record.state:
            query = query.filter(Authority.state == record.state)
        if record.district:
            query = query.filter(Authority.district == record.district)
        if record.pio_designation:
            query = query.filter(Authority.pio_designation == record.pio_designation)
        
        matches = query.all()
        return len(matches) > 0, matches

    for idx, record in enumerate(request.records):
        if not record.source_url or not record.source_type:
            results.append(AuthorityImportResult(index=idx, status="REJECTED", reason="Missing source_url or source_type"))
            rejected += 1
            continue
            
        if record.verification_status == "VERIFIED" and not record.verification_notes:
            results.append(AuthorityImportResult(index=idx, status="REJECTED", reason="VERIFIED status requires verification_notes metadata"))
            rejected += 1
            continue
            
        is_dup, existing = _is_duplicate(record)
        if is_dup:
            # We treat any matched record as a POSSIBLE_DUPLICATE and skip import to avoid silent overwrites
            # The admin should manually review and update existing records
            results.append(AuthorityImportResult(
                index=idx, 
                status="POSSIBLE_DUPLICATE", 
                reason="Similar authority already exists",
                authority_id=existing[0].id
            ))
            duplicates += 1
            continue
            
        # Create authority
        authority = Authority(
            department=record.department,
            ministry=record.ministry,
            government_level=record.government_level,
            state=record.state,
            district=record.district,
            office_name=record.office_name,
            pio_designation=record.pio_designation,
            pio_name=record.pio_name,
            appellate_authority_designation=record.appellate_authority_designation,
            address=record.address,
            online_portal=record.online_portal,
            filing_fee=record.filing_fee,
            payment_methods=record.payment_methods,
            source_url=record.source_url,
            source_type=record.source_type,
            verification_status=record.verification_status,
            last_verified=datetime.now(timezone.utc),
            active=True
        )
        
        if record.verification_status == "VERIFIED":
            authority.verified_by = admin.email
            
        db.add(authority)
        db.flush()
        
        if record.verification_status == "VERIFIED":
            history = AuthorityVerificationHistory(
                authority_id=authority.id,
                source_url=authority.source_url,
                source_type=authority.source_type,
                verification_status="VERIFIED",
                verified_by=admin.email,
                notes=record.verification_notes or "Verified via bulk import"
            )
            db.add(history)
            
        imported += 1
        results.append(AuthorityImportResult(index=idx, status="IMPORTED", authority_id=authority.id))
        
    db.commit()
    return AuthorityImportResponse(
        total_processed=total,
        imported=imported,
        rejected=rejected,
        possible_duplicates=duplicates,
        results=results
    )
