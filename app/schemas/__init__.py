"""
Pydantic schemas for request/response validation
"""
from app.schemas.user import UserBase, UserCreate, UserUpdate, UserResponse, UserLogin
from app.schemas.token import Token, TokenData, RefreshTokenRequest
from app.schemas.location import LocationBase, LocationCreate, LocationUpdate, LocationResponse
from app.schemas.category import CategoryBase, CategoryCreate, CategoryUpdate, CategoryResponse
from app.schemas.invoice import (
    InvoiceStatus,
    InvoiceBase,
    InvoiceCreate,
    InvoiceUpdate,
    InvoiceResponse,
    InvoiceWithImages
)
from app.schemas.invoice_image import (
    InvoiceImageBase,
    InvoiceImageCreate,
    InvoiceImageResponse
)

__all__ = [
    # User
    'UserBase', 'UserCreate', 'UserUpdate', 'UserResponse', 'UserLogin',
    # Location
    'LocationBase', 'LocationCreate', 'LocationUpdate', 'LocationResponse',
    # Category
    'CategoryBase', 'CategoryCreate', 'CategoryUpdate', 'CategoryResponse',
    # Invoice
    'InvoiceStatus', 'InvoiceBase', 'InvoiceCreate', 'InvoiceUpdate',
    'InvoiceResponse', 'InvoiceWithImages',
    # Invoice Image
    'InvoiceImageBase', 'InvoiceImageCreate', 'InvoiceImageResponse',
]
