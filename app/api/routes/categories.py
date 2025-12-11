from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.deps import get_current_user
from app.schemas import category as category_schemas
from app.crud import category as category_crud
from app.models.user import User

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=category_schemas.CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category: category_schemas.CategoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new category"""
    # Check if code already exists
    if category.code:
        db_category = category_crud.get_category_by_code(db, code=category.code)
        if db_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category code already exists"
            )
    
    return category_crud.create_category(db=db, category=category)


@router.get("/", response_model=List[category_schemas.CategoryResponse])
def list_categories(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = Query(False, description="Filter only active categories"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of categories"""
    categories = category_crud.get_categories(db, skip=skip, limit=limit, active_only=active_only)
    return categories



