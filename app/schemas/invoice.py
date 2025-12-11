from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any, TYPE_CHECKING
from datetime import datetime
from enum import Enum
import uuid

if TYPE_CHECKING:
    from app.schemas.invoice_image import InvoiceImageResponse


class InvoiceStatus(str, Enum):
    """Invoice status enumeration"""
    DRAFT = "draft"
    COMPLETED = "completed"
    SYNCED = "synced"


class InvoiceBase(BaseModel):
    """Base invoice schema"""
    location_id: Optional[uuid.UUID] = None
    category_id: Optional[int] = None
    note: Optional[str] = None
    extra_metadata: Dict[str, Any] = Field(default_factory=dict)


class InvoiceCreate(InvoiceBase):
    """Schema for creating a new invoice"""
    status: InvoiceStatus = InvoiceStatus.DRAFT





class InvoiceResponse(InvoiceBase):
    """Schema for invoice responses"""
    id: uuid.UUID
    user_id: uuid.UUID
    status: str
    captured_at: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class InvoiceWithImages(InvoiceResponse):
    """Schema for invoice with images"""
    images: list = Field(default_factory=list)
    
    model_config = ConfigDict(from_attributes=True)

