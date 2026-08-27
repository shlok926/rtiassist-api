from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.database import Base
from models.orm.base import BaseModel, get_utc_now
from models.orm.document import Document
from models.orm.case_event import CaseEvent
from models.orm.authority import Authority
from models.orm.filing import Filing
from models.orm.deadline import Deadline

class Case(Base, BaseModel):
    __tablename__ = "cases"
    
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String, nullable=True)
    problem_description = Column(String, nullable=False)
    status = Column(String, nullable=False, default="UNDERSTANDING", index=True)
    priority = Column(String, nullable=True)
    recommended_action = Column(String, nullable=True)
    
    # Phase 13: Case Intelligence
    case_objective = Column(String, nullable=True)
    extracted_facts = Column(String, nullable=True) # JSON string
    facts_confirmed = Column(String, default="false")
    next_action_recommendation = Column(String, nullable=True)
    
    # Phase 4: Authority Resolution
    authority_id = Column(String, ForeignKey("authorities.id"), nullable=True)
    authority_resolution_status = Column(String, nullable=True)
    authority_resolution_reason = Column(String, nullable=True)
    authority_resolved_at = Column(DateTime(timezone=True), nullable=True)
    
    updated_at = Column(DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now)
    
    user = relationship("User", back_populates="cases")
    documents = relationship("Document", back_populates="case", cascade="all, delete-orphan")
    events = relationship("CaseEvent", back_populates="case", cascade="all, delete-orphan")
    filings = relationship("Filing", back_populates="case", cascade="all, delete-orphan")
    deadlines = relationship("Deadline", back_populates="case", cascade="all, delete-orphan")
    response_analyses = relationship("ResponseAnalysis", back_populates="case", cascade="all, delete-orphan")
    appeals = relationship("Appeal", back_populates="case", cascade="all, delete-orphan")
