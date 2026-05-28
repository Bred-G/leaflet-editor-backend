from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Название проекта")
    xml_content: str = Field(..., description="XML-шаблон листовки")
    page_width: Optional[int] = Field(800, description="Ширина страницы в пикселях")
    page_height: Optional[int] = Field(600, description="Высота страницы в пикселях")

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    xml_content: Optional[str] = None
    page_width: Optional[int] = None
    page_height: Optional[int] = None

class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class ProjectListResponse(BaseModel):
    items: list[ProjectResponse]
    total: int
    page: int
    size: int