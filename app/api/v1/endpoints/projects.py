from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.models.project import Project
from app.core.database import get_db
from app.services.flyer_service import flyer_service
from app.api.deps import get_current_user_optional, get_current_user
from app.models.user import User

router = APIRouter(prefix="/projects", tags=["projects"])

# Создание нового проекта
@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(project: ProjectCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    # Создаем объект модели
    db_project = Project(name=project.name, xml_content=project.xml_content, user_id=current_user.id)
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    return db_project

# Получение всех проектов
@router.get("/", response_model=List[ProjectResponse])
async def get_projects(skip: int = 0, limit: int = 100, current_user: Optional[User] = Depends(get_current_user_optional), db: AsyncSession = Depends(get_db)):
    query = select(Project)
    if current_user:
        query = query.where(Project.user_id == current_user.id)
    else:
        query = query.where(Project.user_id.is_(None))
    query = query.order_by(Project.updated_at.desc())
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    projects = result.scalars().all()
    return projects

# Получение проекта по ID
@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, current_user: Optional[User] = Depends(get_current_user_optional), db: AsyncSession = Depends(get_db)):
    query = select(Project).where(Project.id == project_id)
    result = await db.execute(query)
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id {project_id} not found")
    if project.user_id is not None:
        if not current_user or project.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return project

# Обновление проекта
@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: int, project_update: ProjectUpdate, current_user: Optional[User] = Depends(get_current_user_optional), db: AsyncSession = Depends(get_db)):
    query = select(Project).where(Project.id == project_id)
    result = await db.execute(query)
    db_project = result.scalar_one_or_none()
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id {project_id} not found")
    if db_project.user_id is not None:
        if not current_user or db_project.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    # Обновляем только переданные поля
    update_data = project_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_project, field, value)
    await db.commit()
    await db.refresh(db_project)
    return db_project

# Удаление проекта
@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: int, current_user: Optional[User] = Depends(get_current_user_optional), db: AsyncSession = Depends(get_db)):
    query = select(Project).where(Project.id == project_id)
    result = await db.execute(query)
    db_project = result.scalar_one_or_none()
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id {project_id} not found")
    if db_project.user_id is not None:
        if not current_user or db_project.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    await db.delete(db_project)
    await db.commit()
    return None
