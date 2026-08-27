import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime

def get_utc_now():
    return datetime.now(timezone.utc)

class BaseModel:
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime(timezone=True), default=get_utc_now)
