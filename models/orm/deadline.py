from sqlalchemy import Column, String, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from models.database import Base
from models.orm.base import BaseModel, get_utc_now

class Deadline(Base, BaseModel):
    __tablename__ = "deadlines"
    
    case_id = Column(String, ForeignKey("cases.id"), nullable=False, index=True)
    filing_id = Column(String, ForeignKey("filings.id"), nullable=False)
    
    deadline_type = Column(String, nullable=False) # RTI_RESPONSE, FIRST_APPEAL_ELIGIBILITY, CUSTOM
    trigger_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    status = Column(String, nullable=False, default="UPCOMING") # UPCOMING, DUE_SOON, OVERDUE, COMPLETED
    
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    case = relationship("Case", back_populates="deadlines")
    filing = relationship("Filing", back_populates="deadlines")
