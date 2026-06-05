from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.core.database import get_db
from app.schemas.template import TemplateCreate, TemplateUpdate, TemplateResponse, TemplateListResponse
from app.services.template_service import template_service
from app.api.deps import get_current_user_optional
from app.models.user import User

router = APIRouter(prefix="/templates", tags=["templates"])

# Получение списка шаблонов с фильтрацией и пагинацией
@router.get("/", response_model=TemplateListResponse)
async def get_templates(category: Optional[str] = Query(None, description="Фильтр по категории"), tags: Optional[List[str]] = Query(None, description="Фильтр по тегам"), include_preset: bool = Query(True, description="Включить предустановленные шаблоны"), current_user: Optional[User] = Depends(get_current_user_optional), page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100), db: AsyncSession = Depends(get_db)):  
    skip = (page - 1) * size
    user_id = current_user.id if current_user else None
    templates, total = await template_service.get_templa
    templates, total = await template_service.get_templates(db=db, user_id=user_id, category=category, tags=tags, include_preset=include_preset, skip=skip, limit=size)
    return TemplateListResponse(items=templates, total=total, page=page, size=size, has_more=skip + size < total)

# Получение списка всех категорий
@router.get("/categories", response_model=List[str])
async def get_categories(db: AsyncSession = Depends(get_db)):
    return await template_service.get_categories(db)

# Получение популярных тегов
@router.get("/popular-tags", response_model=List[dict])
async def get_popular_tags(limit: int = Query(20, ge=1, le=50), db: AsyncSession = Depends(get_db)):
    return await template_service.get_popular_tags(db, limit)

# Получение шаблона по ID
@router.get("/{template_id}", response_model=TemplateResponse)
async def get_template(template_id: int, increment_usage: bool = Query(True, description="Увеличить счетчик использования"), current_user: Optional[User] = Depends(get_current_user_optional), db: AsyncSession = Depends(get_db)):
    template = await template_service.get_template_by_id(db, template_id)
    if not template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Template with id {template_id} not found")
    if template.user_id is not None:
        # Пользовательские шаблоны доступны только владельцу
        if not current_user or template.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied. This template belongs to another user.")
    if increment_usage:
        await template_service.increment_usage_count(db, template_id)
        await db.refresh(template)
    return template

# Создание нового шаблона
@router.post("/", response_model=TemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_template(template: TemplateCreate, current_user: Optional[User] = Depends(get_current_user_optional), db: AsyncSession = Depends(get_db)):
    try:
        new_template = await template_service.create_template(db=db, template_data=template, user_id=current_user.id if current_user else None)
        return new_template
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Обновление шаблонов
@router.put("/{template_id}", response_model=TemplateResponse)
async def update_template(template_id: int, template_update: TemplateUpdate, current_user: Optional[User] = Depends(get_current_user_optional), db: AsyncSession = Depends(get_db)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required to update templates")
    updated = await template_service.update_template(db=db, template_id=template_id, template_data=template_update, user_id=current_user.id)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template is not found or you don't have permission to edit it")
    return updated

# Удаление шаблона
@router.delete("/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_template(template_id: int, current_user: Optional[User] = Depends(get_current_user_optional), db: AsyncSession = Depends(get_db)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required to delete templates")
    deleted = await template_service.delete_template(db=db, template_id=template_id, user_id=current_user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template is not found or cannot be deleted")
    return None
