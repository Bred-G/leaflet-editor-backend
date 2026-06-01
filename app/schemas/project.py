from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from app.services.flyer_service import flyer_service

# Базовая схема проекта
class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Название проекта")
    xml_content: str = Field(..., description="XML-шаблон листовки")
    # Валидация XML формата    
    @field_validator('xml_content')
    @classmethod
    def validate_xml(cls, v: str) -> str:
        if not flyer_service.validate_xml(v):
            raise ValueError('Invalid XML format. Root tag must be "flyer"')
        return v

# Схема для создания проекта
class ProjectCreate(ProjectBase):
    pass

# Схема для обновления проекта
class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    xml_content: Optional[str] = None

# Схема для ответа API
class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

# Список проектов с пагинацией
class ProjectListResponse(BaseModel):
    items: list[ProjectResponse]
    total: int
    page: int
    size: int
