from sqlalchemy.orm import Session
from typing import Optional
import uuid

from app.models.location import Location
from app.schemas.location import LocationCreate, LocationUpdate


def get_location(db: Session, location_id: uuid.UUID) -> Optional[Location]:
    """Get a location by ID"""
    return db.query(Location).filter(Location.id == location_id).first()


def get_location_by_code(db: Session, code: str) -> Optional[Location]:
    """Get a location by code"""
    return db.query(Location).filter(Location.code == code).first()


def get_locations(db: Session, skip: int = 0, limit: int = 100) -> list[Location]:
    """Get all locations with pagination"""
    return db.query(Location).offset(skip).limit(limit).all()


def create_location(db: Session, location: LocationCreate) -> Location:
    """Create a new location"""
    db_location = Location(
        name=location.name,
        address=location.address,
        code=location.code,
        gps_latitude=location.gps_latitude,
        gps_longitude=location.gps_longitude
    )
    
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location


def update_location(db: Session, location_id: uuid.UUID, location: LocationUpdate) -> Optional[Location]:
    """Update a location"""
    db_location = get_location(db, location_id)
    if not db_location:
        return None
    
    update_data = location.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_location, field, value)
    
    db.commit()
    db.refresh(db_location)
    return db_location


def delete_location(db: Session, location_id: uuid.UUID) -> bool:
    """Delete a location"""
    db_location = get_location(db, location_id)
    if not db_location:
        return False
    
    db.delete(db_location)
    db.commit()
    return True

