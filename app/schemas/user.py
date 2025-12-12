from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime
import uuid


class UserBase(BaseModel):
    """Base user schema with common fields"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=100)
    avatar_url: Optional[str] = None
    role: str = Field(default='staff', pattern='^(admin|staff)$')


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(..., min_length=8)





class UserResponse(UserBase):
    """Schema for user responses"""
    id: uuid.UUID
    is_active: bool
    last_login_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    """Schema for user login"""
    username: str
    password: str


# Import token schemas for convenience
from app.schemas.token import Token, RefreshTokenRequest

__all__ = [
    'UserBase',
    'UserCreate',
    'UserResponse',
    'UserLogin',
    'Token',
    'RefreshTokenRequest',
]

