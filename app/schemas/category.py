from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class CategoryBase(BaseModel):
    """Base category schema"""
    name: str = Field(..., max_length=100)
    code: Optional[str] = Field(None, max_length=50)
    icon_name: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    """Schema for creating a new category"""
    is_active: bool = True


class CategoryUpdate(BaseModel):
    """Schema for updating category information"""
    name: Optional[str] = Field(None, max_length=100)
    code: Optional[str] = Field(None, max_length=50)
    icon_name: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    is_active: Optional[bool] = None


class CategoryResponse(CategoryBase):
    """Schema for category responses"""
    id: int
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)
