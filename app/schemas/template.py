from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from app.services.flyer_service import flyer_service

# Базовая схема шаблона
class TemplateBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    xml_content: str
    category: Optional[str] = Field(None, max_length=100)
    tags: Optional[List[str]] = Field(default_factory=list)
    preview_url: Optional[str] = None
    # Валидация XML формата
    @field_validator('xml_content')
    @classmethod
    def validate_xml(cls, v: str) -> str:
        if not flyer_service.validate_xml(v):
            raise ValueError('Invalid XML format. Root tag must be "flyer"')
        return v

# Схема для создания шаблона
class TemplateCreate(TemplateBase):
    pass

# Схема для обновления шаблона
class TemplateUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    xml_content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    preview_url: Optional[str] = None

# Схема для ответа API
class TemplateResponse(TemplateBase):
    id: int
    name: str
    xml_content: str
    user_id: Optional[int] = None
    preview_url: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    usage_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True
    # Преобразуем None в пустой список
    @field_validator('tags', mode='before')
    @classmethod
    def validate_tags(cls, v):
        if v is None:
            return []
        return v

# Список шаблонов с пагинацией
class TemplateListResponse(BaseModel):
    items: List[TemplateResponse]
    total: int
    page: int
    size: int
    has_more: bool
