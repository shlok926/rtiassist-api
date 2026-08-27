from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import date
from models.orm.case import Case
from models.orm.filing import Filing
from models.orm.deadline import Deadline
from models.orm.case_event import CaseEvent
from models.schemas import FilingCreate, FilingResponse, CaseTimelineResponse
from services.case_service import get_case
from services.deadline_service import calculate_deadlines, determine_deadline_status

def file_case(db: Session, case_id: str, user_id: str, request: FilingCreate) -> FilingResponse:
    case = get_case(db, case_id, user_id)
    
    if case.status != "READY_TO_FILE":
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot file case in current state: {case.status}. Expected READY_TO_FILE."
        )
        
    # Get the READY_TO_FILE document
    document = next((doc for doc in case.documents if doc.status == "READY_TO_FILE"), None)
    if not document:
        raise HTTPException(status_code=400, detail="No READY_TO_FILE document exists for this case.")
        
    if request.filing_date > date.today():
        raise HTTPException(status_code=400, detail="Filing date cannot be in the future.")
        
    # Prevent duplicate filings
    if any(f.document_id == document.id for f in case.filings):
        raise HTTPException(status_code=400, detail="This document has already been filed.")
        
    # Create Filing
    filing = Filing(
        case_id=case.id,
        document_id=document.id,
        filing_date=request.filing_date,
        filing_method=request.filing_method,
        reference_number=request.reference_number,
        notes=request.notes
    )
    
    # Must add filing to db before calculating deadlines so we can associate it (or we can just associate manually)
    db.add(filing)
    db.flush() # To get filing id if needed, but not necessary since we pass filing object
    
    # Calculate Deadlines
    new_deadlines = calculate_deadlines(db, filing)
    for dl_data in new_deadlines:
        deadline = Deadline(
            case_id=case.id,
            filing_id=filing.id,
            deadline_type=dl_data["deadline_type"],
            trigger_date=dl_data["trigger_date"],
            due_date=dl_data["due_date"],
            status=dl_data["status"]
        )
        db.add(deadline)
        db.add(CaseEvent(
            case_id=case.id,
            event_type="DEADLINE_CREATED",
            description=f"Deadline {dl_data['deadline_type']} created. Due: {dl_data['due_date']}"
        ))
        
    # Update Case Status
    case.status = "AWAITING_RESPONSE"
    
    # Create Events
    db.add(CaseEvent(
        case_id=case.id,
        event_type="CASE_FILED",
        description=f"Case filed via {request.filing_method}",
        event_metadata={"filing_id": filing.id}
    ))
    db.add(CaseEvent(
        case_id=case.id,
        event_type="STATUS_CHANGED",
        description="Case status changed to AWAITING_RESPONSE"
    ))
    
    db.commit()
    db.refresh(filing)
    
    return FilingResponse.model_validate(filing)

def get_case_timeline(db: Session, case_id: str, user_id: str) -> CaseTimelineResponse:
    case = get_case(db, case_id, user_id)
    
    # Update dynamic statuses before returning
    for dl in case.deadlines:
        if not dl.completed_at:
            new_status = determine_deadline_status(dl.due_date)
            if new_status != dl.status:
                dl.status = new_status
                db.commit()
    
    active_filing = case.filings[-1] if case.filings else None
    
    # Get remaining days for the most urgent deadline
    remaining_days = None
    if case.deadlines:
        active_deadlines = [dl for dl in case.deadlines if not dl.completed_at]
        if active_deadlines:
            next_dl = min(active_deadlines, key=lambda d: d.due_date)
            remaining_days = (next_dl.due_date - date.today()).days
    
    return CaseTimelineResponse(
        filing=FilingResponse.model_validate(active_filing) if active_filing else None,
        deadlines=case.deadlines,
        events=case.events,
        current_status=case.status,
        remaining_days=remaining_days
    )
