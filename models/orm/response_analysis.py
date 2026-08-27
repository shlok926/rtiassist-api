from sqlalchemy import Column, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from models.database import Base
from models.orm.base import BaseModel

class ResponseAnalysis(Base, BaseModel):
    __tablename__ = "response_analyses"
    
    case_id = Column(String, ForeignKey("cases.id"), nullable=False, index=True)
    document_id = Column(String, ForeignKey("documents.id"), nullable=False, index=True)
    
    status = Column(String, nullable=False) # ANSWERED, PARTIALLY_ANSWERED, NOT_ANSWERED, DENIED, IRRELEVANT
    answered = Column(JSON, nullable=False) # list of answered points
    not_answered = Column(JSON, nullable=False) # list of unanswered points
    recommended_action = Column(String, nullable=False) # CLOSE_CASE, REQUEST_CLARIFICATION, FOLLOW_UP, FIRST_APPEAL, NEEDS_HUMAN_REVIEW
    request_mapping = Column(JSON, nullable=True) # List of dicts mapping request to response
    
    case = relationship("Case", back_populates="response_analyses")
    document = relationship("Document")
