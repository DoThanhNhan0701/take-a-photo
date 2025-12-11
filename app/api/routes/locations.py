from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.core.database import get_db
from app.core.deps import get_current_user
from app.schemas import location as location_schemas
from app.crud import location as location_crud
from app.models.user import User

router = APIRouter(prefix="/locations", tags=["locations"])


@router.post("/", response_model=location_schemas.LocationResponse, status_code=status.HTTP_201_CREATED)
def create_location(
    location: location_schemas.LocationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new location"""
    # Check if code already exists
    if location.code:
        db_location = location_crud.get_location_by_code(db, code=location.code)
        if db_location:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Location code already exists"
            )
    
    return location_crud.create_location(db=db, location=location)


@router.get("/", response_model=List[location_schemas.LocationResponse])
def list_locations(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of locations"""
    locations = location_crud.get_locations(db, skip=skip, limit=limit)
    return locations









