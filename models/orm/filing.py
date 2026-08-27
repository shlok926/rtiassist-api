from sqlalchemy import Column, String, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from models.database import Base
from models.orm.base import BaseModel, get_utc_now

class Filing(Base, BaseModel):
    __tablename__ = "filings"
    
    case_id = Column(String, ForeignKey("cases.id"), nullable=False, index=True)
    document_id = Column(String, ForeignKey("documents.id"), nullable=False)
    
    filing_date = Column(Date, nullable=False)
    filing_method = Column(String, nullable=False) # ONLINE, POSTAL, IN_PERSON, EMAIL, OTHER
    reference_number = Column(String, nullable=True)
    acknowledgement_number = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    
    case = relationship("Case", back_populates="filings")
    document = relationship("Document")
    deadlines = relationship("Deadline", back_populates="filing", cascade="all, delete-orphan")
