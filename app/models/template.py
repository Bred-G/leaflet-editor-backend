from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, ARRAY, Index
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql import func
from app.core.database import Base

class Template(Base):
    __tablename__ = "templates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    xml_content = Column(Text, nullable=False)
    is_preset = Column(Boolean, default=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    preview_url = Column(String(500), nullable=True)
    category = Column(String(100), nullable=True, index=True)
    tags = Column(ARRAY(String), nullable=True, default=[])
    usage_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    __table_args__ = (Index('idx_templates_user_category', 'user_id', 'category'), Index('idx_templates_preset_category', 'is_preset', 'category'))

    def __repr__(self):
        return f"<Template(id={self.id}, name='{self.name}', is_preset={self.is_preset})>"
