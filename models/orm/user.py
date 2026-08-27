from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from models.database import Base
from models.orm.base import BaseModel, get_utc_now

class User(Base, BaseModel):
    __tablename__ = "users"
    
    # Original minimal fields
    telegram_id = Column(String, unique=True, index=True, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    
    # Phase 9: Authentication & Profile
    email = Column(String, unique=True, index=True, nullable=True)
    password_hash = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(String, default="USER") # USER or ADMIN
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    
    updated_at = Column(DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now)
    
    cases = relationship("Case", back_populates="user", cascade="all, delete-orphan")
