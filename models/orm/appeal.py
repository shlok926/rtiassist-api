from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.database import Base
from models.orm.base import BaseModel, get_utc_now

class Appeal(Base, BaseModel):
    __tablename__ = "appeals"
    
    case_id = Column(String, ForeignKey("cases.id"), nullable=False, index=True)
    appeal_type = Column(String, nullable=False, default="FIRST_APPEAL")
    status = Column(String, nullable=False, default="RECOMMENDED") # RECOMMENDED, CONFIRMED, AUTHORITY_RESOLUTION, DRAFTING, QUALITY_CHECK, READY_TO_FILE, FILED, AWAITING_RESPONSE, CLOSED
    
    parent_document_id = Column(String, ForeignKey("documents.id"), nullable=False) # The original RTI
    parent_response_document_id = Column(String, ForeignKey("documents.id"), nullable=False) # The government response
    response_analysis_id = Column(String, ForeignKey("response_analyses.id"), nullable=False)
    
    appellate_authority_id = Column(String, ForeignKey("authorities.id"), nullable=True)
    
    updated_at = Column(DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now)
    
    case = relationship("Case", back_populates="appeals")
    
    parent_document = relationship("Document", foreign_keys=[parent_document_id])
    parent_response_document = relationship("Document", foreign_keys=[parent_response_document_id])
    response_analysis = relationship("ResponseAnalysis", foreign_keys=[response_analysis_id])
    appellate_authority = relationship("Authority", foreign_keys=[appellate_authority_id])
