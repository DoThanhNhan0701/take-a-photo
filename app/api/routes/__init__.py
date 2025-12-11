"""
API Routes
"""
from fastapi import APIRouter
from app.api.routes import auth, users, locations, categories, invoices, invoice_images

# Create main API router
api_router = APIRouter()

# Include all sub-routers
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(locations.router)
api_router.include_router(categories.router)
api_router.include_router(invoices.router)
api_router.include_router(invoice_images.router)

__all__ = ['api_router']

