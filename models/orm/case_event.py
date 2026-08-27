from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import json
from models.database import Base
from models.orm.base import BaseModel

class CaseEvent(Base, BaseModel):
    __tablename__ = "case_events"
    
    case_id = Column(String, ForeignKey("cases.id"), nullable=False, index=True)
    event_type = Column(String, nullable=False)
    description = Column(String, nullable=False)
    metadata_json = Column(String, nullable=True) # Storing arbitrary metadata as JSON string
    
    case = relationship("Case", back_populates="events")

    @property
    def event_metadata(self):
        if self.metadata_json:
            return json.loads(self.metadata_json)
        return None

    @event_metadata.setter
    def event_metadata(self, value):
        if value:
            self.metadata_json = json.dumps(value)
        else:
            self.metadata_json = None
