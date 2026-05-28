from fastapi import APIRouter
from app.api.v1.endpoints import projects, export

api_router = APIRouter()

api_router.include_router(projects.router)
api_router.include_router(export.router)