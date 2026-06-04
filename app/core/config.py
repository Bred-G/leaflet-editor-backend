from pydantic_settings import BaseSettings
from typing import Optional

#Настройки приложения
class Settings(BaseSettings):
    APP_NAME: str = "Leaflet Editor API"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    # Настройки базы данных
    DATABASE_URL: str
    DATABASE_URL_SYNC: Optional[str] = None
    # JWT настройки
    SECRET_KEY: str = "8f7a9e2b4c1d6h3j5k8l2m4n6p9r1t3v5w7y0z2x4c6v8b0n2m4p6r8t0v2x4z6b8"	# Значение по умолчанию
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    # Настройки CORS
    ALLOWED_ORIGINS: list = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
