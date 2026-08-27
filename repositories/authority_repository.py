from typing import List, Optional
from sqlalchemy.orm import Session
from models.orm.authority import Authority
from sqlalchemy import or_

def get_by_id(db: Session, authority_id: str) -> Optional[Authority]:
    return db.query(Authority).filter(Authority.id == authority_id).first()

def search(
    db: Session, 
    department: Optional[str] = None,
    ministry: Optional[str] = None,
    government_level: Optional[str] = None,
    state: Optional[str] = None,
    district: Optional[str] = None,
    verification_status: Optional[str] = None,
    active: bool = True
) -> List[Authority]:
    query = db.query(Authority).filter(Authority.active == active)
    
    if government_level:
        query = query.filter(Authority.government_level == government_level.upper())
    if state:
        query = query.filter(Authority.state.ilike(f"%{state}%"))
    if district:
        query = query.filter(Authority.district.ilike(f"%{district}%"))
    if verification_status:
        query = query.filter(Authority.verification_status == verification_status.upper())
    
    if department:
        query = query.filter(Authority.department.ilike(f"%{department}%"))
    if ministry:
        query = query.filter(Authority.ministry.ilike(f"%{ministry}%"))
        
    return query.all()
    
def create(db: Session, authority: Authority) -> Authority:
    db.add(authority)
    db.commit()
    db.refresh(authority)
    return authority
