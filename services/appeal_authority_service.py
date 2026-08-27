from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.orm.appeal import Appeal
from models.orm.authority import Authority
from models.orm.case_event import CaseEvent
from services.appeal_service import get_appeal

def resolve_appellate_authority(db: Session, case_id: str, appeal_id: str, user_id: str):
    appeal = get_appeal(db, case_id, appeal_id, user_id)
    
    if appeal.status != "CONFIRMED":
        raise HTTPException(status_code=400, detail="Appeal must be CONFIRMED to resolve authority.")
        
    case = appeal.case
    original_authority = case.authority_id
    
    if not original_authority:
        raise HTTPException(status_code=400, detail="Case has no original authority.")
        
    auth = db.query(Authority).filter(Authority.id == original_authority).first()
    
    # In a real system, we'd query for the First Appellate Authority associated with this department.
    # For deterministic mock, we will just assign the same authority record, assuming it has FAA details.
    
    appeal.appellate_authority_id = auth.id
    appeal.status = "APPEAL_AUTHORITY_RESOLVED"
    case.status = "APPEAL_AUTHORITY_RESOLVED"
    
    db.add(CaseEvent(
        case_id=case.id,
        event_type="APPEAL_AUTHORITY_RESOLVED",
        description=f"Resolved Appellate Authority for {auth.department}",
        event_metadata={"authority_id": auth.id}
    ))
    
    db.commit()
    db.refresh(appeal)
    
    from models.schemas import AppealResponse
    return AppealResponse.model_validate(appeal)
