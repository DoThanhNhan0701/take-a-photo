from sqlalchemy.orm import Session
from typing import Optional

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


def get_category(db: Session, category_id: int) -> Optional[Category]:
    """Get a category by ID"""
    return db.query(Category).filter(Category.id == category_id).first()


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


def update_category(db: Session, category_id: int, category: CategoryUpdate) -> Optional[Category]:
    """Update a category"""
    db_category = get_category(db, category_id)
    if not db_category:
        return None
    
    update_data = category.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_category, field, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int) -> bool:
    """Delete a category"""
    db_category = get_category(db, category_id)
    if not db_category:
        return False
    
    db.delete(db_category)
    db.commit()
    return True
