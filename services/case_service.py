from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.orm.case import Case
from models.orm.case_event import CaseEvent
from models.schemas import CaseCreate, CaseUpdate, ActionRecommendation, ActionConfirmation, AuthorityResolution
from repositories import case_repository, case_event_repository
from agents import action_recommender
from services import authority_service
from datetime import datetime, timezone

def create_case(db: Session, user_id: str, case_data: CaseCreate) -> Case:
    # 1. Create Case
    new_case = Case(
        user_id=user_id,
        problem_description=case_data.problem_description,
        title=case_data.title,
        status="UNDERSTANDING"
    )
    # Don't commit yet to keep it atomic if we want, but case_repository.create commits.
    # We will let case_repository commit and then add the event.
    # For full atomicity in real production, we'd add both to session and commit once.
    # Let's adjust to do atomic commit here:
    
    db.add(new_case)
    db.flush() # Get the new_case.id without committing
    
    # 2. Create Event
    event = CaseEvent(
        case_id=new_case.id,
        event_type="CASE_CREATED",
        description="Case was initialized."
    )
    db.add(event)
    
    db.commit()
    db.refresh(new_case)
    return new_case

def get_case(db: Session, case_id: str, user_id: str) -> Case:
    case = case_repository.get_by_id(db, case_id, user_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found or access denied")
    return case

def get_cases(db: Session, user_id: str, skip: int = 0, limit: int = 100) -> dict:
    cases = db.query(Case).filter(Case.user_id == user_id).order_by(Case.created_at.desc()).offset(skip).limit(limit).all()
    total = db.query(Case).filter(Case.user_id == user_id).count()
    
    # Calculate Phase 6 summary fields for the list response
    case_responses = []
    for c in cases:
        # Use a dict mapped manually to ensure all ORM properties are properly copied
        c_dict = {
            "id": c.id,
            "status": c.status,
            "problem_description": c.problem_description,
            "title": c.title,
            "priority": c.priority,
            "recommended_action": c.recommended_action,
            "created_at": c.created_at,
            "updated_at": c.updated_at,
            "events": c.events,
            "documents": c.documents,
            "case_objective": c.case_objective,
            "extracted_facts": c.extracted_facts,
            "facts_confirmed": c.facts_confirmed,
            "next_action_recommendation": c.next_action_recommendation,
        }
        
        # Determine active filing
        active_filing = c.filings[-1] if c.filings else None
        print(f"CASE {c.id} FILINGS: {c.filings}")
        if active_filing:
            c_dict["filing_date"] = active_filing.filing_date
            
        # Determine deadlines
        active_deadlines = [dl for dl in c.deadlines if not dl.completed_at]
        if active_deadlines:
            next_dl = min(active_deadlines, key=lambda d: d.due_date)
            from datetime import date
            c_dict["next_deadline"] = next_dl.due_date
            c_dict["remaining_days"] = (next_dl.due_date - date.today()).days
            c_dict["overdue"] = c_dict["remaining_days"] < 0
            
        case_responses.append(c_dict)
        
    return {"cases": case_responses, "total": total}

def list_cases(db: Session, user_id: str, skip: int = 0, limit: int = 100):
    return case_repository.list_for_user(db, user_id, skip, limit)

def update_case(db: Session, case_id: str, user_id: str, update_data: CaseUpdate) -> Case:
    case = get_case(db, case_id, user_id)
    
    changes = []
    if update_data.title is not None and case.title != update_data.title:
        case.title = update_data.title
        changes.append("Title updated")
        
    if update_data.status is not None and case.status != update_data.status:
        valid_statuses = ["UNDERSTANDING", "ACTION_RECOMMENDED", "DRAFTING", "READY_TO_FILE", "FILED", "RESPONSE_RECEIVED", "ANALYSIS_READY", "APPEAL_RECOMMENDED", "CLOSED"]
        if update_data.status not in valid_statuses:
            raise HTTPException(status_code=400, detail="Invalid status")
        case.status = update_data.status
        changes.append(f"Status changed to {update_data.status}")
        
    if update_data.priority is not None and case.priority != update_data.priority:
        case.priority = update_data.priority
        changes.append(f"Priority changed to {update_data.priority}")

    if update_data.case_objective is not None and case.case_objective != update_data.case_objective:
        case.case_objective = update_data.case_objective
        changes.append("Case objective updated")
        
    if update_data.extracted_facts is not None and case.extracted_facts != update_data.extracted_facts:
        case.extracted_facts = update_data.extracted_facts
        changes.append("Extracted facts updated")
        
    if update_data.facts_confirmed is not None and case.facts_confirmed != update_data.facts_confirmed:
        case.facts_confirmed = update_data.facts_confirmed
        changes.append(f"Facts confirmed status changed to {update_data.facts_confirmed}")

    if changes:
        event = CaseEvent(
            case_id=case.id,
            event_type="STATUS_CHANGED" if update_data.status else "CASE_UPDATED",
            description=", ".join(changes)
        )
        db.add(event)
        
    db.commit()
    db.refresh(case)
    return case

def recommend_action(db: Session, case_id: str, user_id: str) -> ActionRecommendation:
    case = get_case(db, case_id, user_id)
    
    # Analyze using LLM
    recommendation_dict = action_recommender.recommend_action(case.problem_description)
    recommendation = ActionRecommendation(**recommendation_dict)
    
    # Store recommendation
    import json
    case.recommended_action = recommendation.recommended_action
    case.case_objective = recommendation.objective
    if recommendation.extracted_facts:
        case.extracted_facts = json.dumps(recommendation.extracted_facts)
    
    # Determine Status & Event
    if recommendation.recommended_action == "NEEDS_CLARIFICATION":
        event_type = "ACTION_CLARIFICATION_REQUIRED"
        case.status = "UNDERSTANDING"
    else:
        event_type = "ACTION_RECOMMENDED"
        case.status = "ACTION_RECOMMENDED"
        
    event = CaseEvent(
        case_id=case.id,
        event_type=event_type,
        description=f"Action Recommended: {recommendation.recommended_action}",
        event_metadata={
            "confidence": recommendation.confidence,
            "supported": recommendation.supported
        }
    )
    db.add(event)
    db.commit()
    db.refresh(case)
    
    return recommendation

def confirm_action(db: Session, case_id: str, user_id: str, confirmation: ActionConfirmation) -> Case:
    case = get_case(db, case_id, user_id)
    
    if case.status != "ACTION_RECOMMENDED":
        raise HTTPException(status_code=400, detail=f"Case must be in ACTION_RECOMMENDED state to confirm an action. Current state: {case.status}")
        
    case.recommended_action = confirmation.action
    case.status = "ACTION_CONFIRMED"
    
    event = CaseEvent(
        case_id=case.id,
        event_type="ACTION_CONFIRMED",
        description=f"User confirmed action: {confirmation.action}",
        event_metadata={"confirmed_action": confirmation.action}
    )
    db.add(event)
    db.commit()
    db.refresh(case)
    
    return case

def resolve_case_authority(db: Session, case_id: str, user_id: str) -> AuthorityResolution:
    case = get_case(db, case_id, user_id)
    
    if case.status != "ACTION_CONFIRMED":
        raise HTTPException(status_code=400, detail="Case must be in ACTION_CONFIRMED state to resolve authority.")
        
    resolution = authority_service.resolve_authority_for_case(db, case.problem_description)
    
    case.authority_resolution_status = resolution.match_status
    case.authority_resolution_reason = resolution.reason
    case.authority_resolved_at = datetime.now(timezone.utc)
    
    if resolution.match_status == "MATCHED":
        case.authority_id = resolution.authority_id
        case.status = "AUTHORITY_RESOLVED"
        event_type = "AUTHORITY_RESOLVED"
    elif resolution.match_status == "NEEDS_REVIEW":
        case.authority_id = resolution.authority_id
        case.status = "AUTHORITY_REVIEW_REQUIRED"
        event_type = "AUTHORITY_REVIEW_REQUIRED"
    else:
        # MULTIPLE_MATCHES or NO_MATCH
        event_type = "AUTHORITY_RESOLUTION_FAILED"
        
    event = CaseEvent(
        case_id=case.id,
        event_type=event_type,
        description=f"Authority Resolution: {resolution.match_status}",
        event_metadata={"reason": resolution.reason, "authority_id": resolution.authority_id}
    )
    db.add(event)
    db.commit()
    db.refresh(case)
    
    return resolution

def import_legacy_tracker(db: Session, user_id: str, legacy_data: dict) -> Case:
    # 1. Create Case mapped from legacy
    status_map = {
        "pending": "READY_TO_FILE",
        "filed": "FILED",
        "received": "RESPONSE_RECEIVED",
        "rejected": "RESPONSE_RECEIVED",
        "closed": "CLOSED"
    }
    mapped_status = status_map.get(legacy_data.get("status"), "UNDERSTANDING")
    
    new_case = Case(
        user_id=user_id,
        problem_description=legacy_data.get("description", "Imported from legacy tracker"),
        title=legacy_data.get("department", "Legacy RTI"),
        status=mapped_status
    )
    
    db.add(new_case)
    db.flush()
    
    event = CaseEvent(
        case_id=new_case.id,
        event_type="CASE_IMPORTED",
        description="Case imported from legacy local storage.",
        event_metadata={"legacy_id": legacy_data.get("id"), "legacy_date": legacy_data.get("date")}
    )
    db.add(event)
    
    db.commit()
    db.refresh(new_case)
    return new_case
