from sqlalchemy import Column, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from models.database import Base
from models.orm.base import BaseModel, get_utc_now

class Document(Base, BaseModel):
    __tablename__ = "documents"
    
    case_id = Column(String, ForeignKey("cases.id"), nullable=False, index=True)
    document_type = Column(String, nullable=False) # e.g. RTI, RESPONSE, APPEAL
    title = Column(String, nullable=True)
    status = Column(String, nullable=False, default="DRAFTING") # DRAFTING, GENERATED, QUALITY_CHECKED, NEEDS_REVISION, READY_TO_FILE
    content = Column(String, nullable=True) # Text content if generated
    language = Column(String, nullable=False, default="english")
    quality_score = Column(String, nullable=True) # Int stored as string or just String
    authority_snapshot = Column(String, nullable=True) # JSON string of authority at generation time
    file_path = Column(String, nullable=True) # Path if uploaded file
    mime_type = Column(String, nullable=True)
    extraction_metadata = Column(JSON, nullable=True) # e.g. {"ocr_used": true, "method": "OCR", "page_count": 4}
    
    # Phase 13 Provenance
    generation_context = Column(JSON, nullable=True)
    generated_from_case_version = Column(String, nullable=True)
    quality_check_result = Column(JSON, nullable=True)
    
    version = Column(String, nullable=False, default="v1")
    
    updated_at = Column(DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now)
    
    case = relationship("Case", back_populates="documents")
