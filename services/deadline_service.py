from datetime import timedelta, date
from typing import List
from sqlalchemy.orm import Session
from models.orm.filing import Filing
from models.orm.deadline import Deadline
from models.orm.deadline_rule import DeadlineRule

def get_or_create_rule(db: Session, event_type: str) -> DeadlineRule:
    rule = db.query(DeadlineRule).filter(DeadlineRule.event_type == event_type, DeadlineRule.verification_status == "VERIFIED").first()
    if rule:
        return rule
        
    # Seed default rule if missing
    duration = 30
    source = "Section 7(1) of RTI Act 2005"
    if event_type == "FIRST_APPEAL_RESPONSE":
        duration = 45 # max 45 days typically 30+15
        source = "Section 19(6) of RTI Act 2005"
        
    rule = DeadlineRule(
        event_type=event_type,
        duration_days=duration,
        source_url="https://rti.gov.in/rti-act.pdf",
        source_type=source
    )
    db.add(rule)
    db.flush()
    return rule

def calculate_deadlines(db: Session, filing: Filing) -> List[dict]:
    """
    Deterministically calculate response deadlines based on the filing date and Rule.
    """
    deadlines = []
    
    # Determine the correct rule event type
    event_type = "RTI_RESPONSE"
    document_type = None
    if filing.document:
        document_type = filing.document.document_type
    else:
        from models.orm.document import Document
        doc = db.query(Document).filter(Document.id == filing.document_id).first()
        if doc:
            document_type = doc.document_type
            
    if document_type == "FIRST_APPEAL":
        event_type = "FIRST_APPEAL_RESPONSE"
        
    rule = get_or_create_rule(db, event_type)
    
    trigger_date = filing.filing_date
    due_date = trigger_date + timedelta(days=rule.duration_days)
    
    deadlines.append({
        "deadline_type": event_type,
        "trigger_date": trigger_date,
        "due_date": due_date,
        "status": determine_deadline_status(due_date)
    })
    
    return deadlines

def determine_deadline_status(due_date: date) -> str:
    """
    Deterministically computes deadline status based on the current date.
    """
    today = date.today()
    days_remaining = (due_date - today).days
    
    if days_remaining < 0:
        return "OVERDUE"
    elif days_remaining <= 7:
        return "DUE_SOON"
    else:
        return "UPCOMING"
