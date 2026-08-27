from sqlalchemy.orm import Session
from models.orm.case_event import CaseEvent

def create(db: Session, event: CaseEvent) -> CaseEvent:
    db.add(event)
    db.commit()
    db.refresh(event)
    return event
