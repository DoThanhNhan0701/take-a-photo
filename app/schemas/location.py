from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
import uuid


class LocationBase(BaseModel):
    """Base location schema"""
    name: str = Field(..., max_length=255)
    address: Optional[str] = None
    code: Optional[str] = Field(None, max_length=50)
    gps_latitude: Optional[float] = Field(None, ge=-90, le=90)
    gps_longitude: Optional[float] = Field(None, ge=-180, le=180)


class LocationCreate(LocationBase):
    """Schema for creating a new location"""
    pass


class LocationUpdate(BaseModel):
    """Schema for updating location information"""
    name: Optional[str] = Field(None, max_length=255)
    address: Optional[str] = None
    code: Optional[str] = Field(None, max_length=50)
    gps_latitude: Optional[float] = Field(None, ge=-90, le=90)
    gps_longitude: Optional[float] = Field(None, ge=-180, le=180)


class LocationResponse(LocationBase):
    """Schema for location responses"""
    id: uuid.UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
