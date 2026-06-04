from pydantic import BaseModel, Field, field_validator
from typing import Optional

# Схема для регистрации пользователя
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=3, max_length=72)

# Схема для входа пользователя
class UserLogin(BaseModel):
    username: str
    password: str

# Схема для ответа с данными пользователя
class UserResponse(BaseModel):
    id: int
    username: str
    class Config:
        from_attributes = True

# Схема для JWT токена
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

# Данные внутри токена
class TokenData(BaseModel):
    user_id: int
    username: str