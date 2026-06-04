from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime, timezone
from app.core.database import Base
import uuid

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    xml_content = Column(Text, nullable=False)
    user_id = Column(Integer, nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
