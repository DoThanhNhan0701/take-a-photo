from sqlalchemy.orm import Session
from typing import Optional

from app.models.category import Category
from app.schemas.category import CategoryCreate


def get_category_by_code(db: Session, code: str) -> Optional[Category]:
    """Get a category by code"""
    return db.query(Category).filter(Category.code == code).first()


def get_categories(db: Session, skip: int = 0, limit: int = 100, active_only: bool = False) -> list[Category]:
    """Get all categories with pagination"""
    query = db.query(Category)
    if active_only:
        query = query.filter(Category.is_active == True)
    return query.offset(skip).limit(limit).all()


def create_category(db: Session, category: CategoryCreate) -> Category:
    """Create a new category"""
    db_category = Category(
        name=category.name,
        code=category.code,
        icon_name=category.icon_name,
        description=category.description,
        is_active=category.is_active
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category
