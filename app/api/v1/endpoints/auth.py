from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.schemas.auth import UserCreate, UserLogin, UserResponse, Token
from app.models.user import User
from app.core.config import settings
from app.api.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

# Регистрация нового пользователя
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # Проверка существующего пользователя
    result = await db.execute(select(User).where(User.username == user_data.username))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
    # Создание пользователя
    new_user = User(username=user_data.username, password_hash=get_password_hash(user_data.password))
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# Вход пользователя
@router.post("/login", response_model=Token)
async def login(login_data: UserLogin, db: AsyncSession = Depends(get_db)):
    # Поиск пользователя
    result = await db.execute(select(User).where(User.username == login_data.username))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    # Создаем токен
    access_token = create_access_token(
        data={
            "user_id": user.id,
            "username": user.username
        }
    )
    return Token(access_token=access_token, token_type="bearer", expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)

# Получить информацию о текущем пользователе
@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

# Выход из системы
@router.post("/logout")
async def logout():
    return {"message": "Successfully logged out"}
