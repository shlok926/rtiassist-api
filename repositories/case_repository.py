from typing import List, Optional
from sqlalchemy.orm import Session
from models.orm.case import Case

def create(db: Session, case: Case) -> Case:
    db.add(case)
    db.commit()
    db.refresh(case)
    return case

def get_by_id(db: Session, case_id: str, user_id: str) -> Optional[Case]:
    return db.query(Case).filter(Case.id == case_id, Case.user_id == user_id).first()

def list_for_user(db: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[Case]:
    return db.query(Case).filter(Case.user_id == user_id).order_by(Case.created_at.desc()).offset(skip).limit(limit).all()

def update(db: Session, case: Case) -> Case:
    db.commit()
    db.refresh(case)
    return case

def count_for_user(db: Session, user_id: str) -> int:
    return db.query(Case).filter(Case.user_id == user_id).count()
