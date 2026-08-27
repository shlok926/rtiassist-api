from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from models.database import Base
from sqlalchemy.orm import relationship
from models.orm.base import BaseModel, get_utc_now

class Authority(Base, BaseModel):
    __tablename__ = "authorities"
    
    government_level = Column(String, nullable=False, index=True) # CENTRAL, STATE
    country = Column(String, default="India")
    state = Column(String, nullable=True, index=True)
    district = Column(String, nullable=True, index=True)
    ministry = Column(String, nullable=True, index=True)
    department = Column(String, nullable=False, index=True)
    office_name = Column(String, nullable=True)
    
    pio_designation = Column(String, nullable=True)
    pio_name = Column(String, nullable=True)
    appellate_authority_designation = Column(String, nullable=True)
    address = Column(String, nullable=True)
    filing_fee = Column(String, nullable=True)
    payment_methods = Column(String, nullable=True) # JSON string or comma-separated
    online_portal = Column(String, nullable=True)
    
    # Provenance
    source_url = Column(String, nullable=False)
    source_title = Column(String, nullable=True)
    source_type = Column(String, nullable=False) # OFFICIAL_GOVERNMENT_PORTAL, etc.
    last_verified = Column(DateTime(timezone=True), nullable=False)
    verification_status = Column(String, nullable=False, default="UNVERIFIED", index=True) # VERIFIED, NEEDS_REVIEW, UNVERIFIED, EXPIRED, REJECTED
    verified_by = Column(String, nullable=True)
    active = Column(Boolean, default=True, index=True)
    
    updated_at = Column(DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now)
    
    verification_history = relationship("AuthorityVerificationHistory", back_populates="authority", cascade="all, delete-orphan")

class AuthorityVerificationHistory(Base, BaseModel):
    __tablename__ = "authority_verification_history"
    
    authority_id = Column(String, ForeignKey("authorities.id"), nullable=False, index=True)
    source_url = Column(String, nullable=False)
    source_type = Column(String, nullable=False)
    verification_status = Column(String, nullable=False)
    verified_at = Column(DateTime(timezone=True), default=get_utc_now)
    verified_by = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    
    authority = relationship("Authority", back_populates="verification_history")
