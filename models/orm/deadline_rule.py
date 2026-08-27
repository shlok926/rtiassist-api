from sqlalchemy import Column, String, Integer, DateTime
from models.database import Base
from models.orm.base import BaseModel, get_utc_now

class DeadlineRule(Base, BaseModel):
    __tablename__ = "deadline_rules"
    
    event_type = Column(String, nullable=False, index=True) # e.g. RTI_RESPONSE, FIRST_APPEAL_RESPONSE
    duration_days = Column(Integer, nullable=False)
    
    source_url = Column(String, nullable=True)
    source_type = Column(String, nullable=False) # e.g. RTI_ACT_2005
    effective_from = Column(DateTime(timezone=True), nullable=True)
    effective_until = Column(DateTime(timezone=True), nullable=True)
    verification_status = Column(String, nullable=False, default="VERIFIED")
    
    updated_at = Column(DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now)
