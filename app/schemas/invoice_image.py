from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal
import uuid


class InvoiceImageBase(BaseModel):
    """Base invoice image schema"""
    file_path: str
    file_name: Optional[str] = Field(None, max_length=255)
    file_size: Optional[int] = None
    mime_type: Optional[str] = Field(None, max_length=50)
    gps_latitude: Optional[Decimal] = None
    gps_longitude: Optional[Decimal] = None


class InvoiceImageCreate(InvoiceImageBase):
    """Schema for creating a new invoice image"""
    invoice_id: uuid.UUID


class InvoiceImageResponse(InvoiceImageBase):
    """Schema for invoice image responses"""
    id: uuid.UUID
    invoice_id: uuid.UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
