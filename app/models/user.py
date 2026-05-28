from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"
    full_name = Column(String, nullable=True)
    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")