from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.models.project import Project
from app.core.database import get_db
from app.services.flyer_service import flyer_service

router = APIRouter(prefix="/projects", tags=["projects"])

# Создание нового проекта
@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(project: ProjectCreate, db: AsyncSession = Depends(get_db)):
    # Если размеры страницы не переданы, извлекаем из XML
    page_width = project.page_width
    page_height = project.page_height
    if page_width is None or page_height is None:
        page_width, page_height = flyer_service.get_page_size(project.xml_content)
    # Создаем объект модели
    db_project = Project(name=project.name, xml_content=project.xml_content, page_width=project.page_width, page_height=project.page_height)
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    return db_project

# Получение всех проектов
@router.get("/", response_model=List[ProjectResponse])
async def get_projects(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    query = select(Project).offset(skip).limit(limit)
    result = await db.execute(query)
    projects = result.scalars().all()
    return projects

# Получение проекта по ID
@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Project).where(Project.id == project_id)
    result = await db.execute(query)
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id {project_id} not found")
    return project

# Обновление проекта
@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: int, project_update: ProjectUpdate, db: AsyncSession = Depends(get_db)):
    query = select(Project).where(Project.id == project_id)
    result = await db.execute(query)
    db_project = result.scalar_one_or_none()
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id {project_id} not found")
    # Обновляем только переданные поля
    update_data = project_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_project, field, value)
    await db.commit()
    await db.refresh(db_project)
    return db_project

# Удаление проекта
@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Project).where(Project.id == project_id)
    result = await db.execute(query)
    db_project = result.scalar_one_or_none()
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id {project_id} not found")
    await db.delete(db_project)
    await db.commit()
    return None
