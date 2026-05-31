from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import api_router
from app.services.template_service import template_service
from app.core.database import AsyncSessionLocal

app = FastAPI(
    title="Leaflet Editor API",
    description="API для создания и экспорта листовок на основе XML-шаблонов",
    version="1.0.0",
    docs_url="/api/docs",      # Swagger документация
    redoc_url="/api/redoc",    # ReDoc документация
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # адреса фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Leaflet Editor API is running",
        "docs": "/api/docs",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Инициализация предустановленных шаблонов при старте
@app.on_event("startup")
async def startup_event():
    async with AsyncSessionLocal() as db:
        count = await template_service.initialize_preset_templates(db)
        print(f"Initialized {count} preset templates")

app.include_router(api_router, prefix="/api/v1")
