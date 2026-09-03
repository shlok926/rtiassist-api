from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from models.database import Base
from models.orm.base import BaseModel

class OfficialAuthoritySource(Base, BaseModel):
    __tablename__ = "official_authority_sources"
    
    authority_id = Column(String, ForeignKey("authorities.id"), nullable=False, index=True)
    source_url = Column(String, nullable=False, index=True)
    source_type = Column(String, nullable=False) # OFFICIAL_WEBSITE, RTI_PORTAL, GAZETTE
    
    is_active = Column(Boolean, default=True)
    
    last_fetch_status = Column(String, nullable=True) # SUCCESS, FAILED, TIMEOUT, UNAVAILABLE
    last_fetch_error = Column(String, nullable=True)
    last_successful_fetch_at = Column(DateTime(timezone=True), nullable=True)
    last_checked_at = Column(DateTime(timezone=True), nullable=True)
    
    # Scheduling & Monitoring
    next_check_at = Column(DateTime(timezone=True), nullable=True, index=True)
    consecutive_failures = Column(Integer, default=0)
    is_locked = Column(Boolean, default=False, index=True)
    locked_at = Column(DateTime(timezone=True), nullable=True)
    
    # Parsing & Intelligence
    last_parse_status = Column(String, nullable=True) # PARSED, UNPARSEABLE, UNSUPPORTED
    last_content_hash = Column(String, nullable=True)
    last_extracted_text = Column(String, nullable=True)
    previous_extracted_text = Column(String, nullable=True)
    
    # Review Queue State
    review_status = Column(String, default="UP_TO_DATE", index=True) # UP_TO_DATE, POTENTIAL_CHANGE_REQUIRES_REVIEW
    
    # Relationships
    proposed_changes = relationship("ProposedAuthorityChange", back_populates="source", cascade="all, delete-orphan")


class ProposedAuthorityChange(BaseModel, Base):
    __tablename__ = "proposed_authority_changes"
    
    source_id = Column(String, ForeignKey("official_authority_sources.id"), index=True, nullable=False)
    authority_id = Column(String, ForeignKey("authorities.id"), index=True, nullable=False)
    
    field_name = Column(String, nullable=False) # e.g., "pio_name", "filing_fee", "online_portal"
    old_value = Column(String, nullable=True)
    proposed_value = Column(String, nullable=True)
    evidence_snippet = Column(String, nullable=True)
    
    change_type = Column(String, nullable=False) # ADDED, CHANGED, REMOVED, AMBIGUOUS, UNEXTRACTABLE
    confidence = Column(String, nullable=False) # HIGH, AMBIGUOUS, LOW
    review_status = Column(String, default="PENDING_REVIEW", index=True) # PENDING_REVIEW, ACCEPTED, REJECTED, MARKED_AMBIGUOUS
    
    # Audit trail
    reviewed_by = Column(String, nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    review_notes = Column(String, nullable=True)
    
    # Relationships
    source = relationship("OfficialAuthoritySource", back_populates="proposed_changes")
    
    authority = relationship("Authority", backref="official_sources")
