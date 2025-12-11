from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.core.database import get_db
from app.core.deps import get_current_user
from app.schemas import invoice_image as image_schemas
from app.crud import invoice_image as image_crud
from app.models.user import User

router = APIRouter(prefix="/invoice-images", tags=["invoice-images"])


@router.post("/", response_model=image_schemas.InvoiceImageResponse, status_code=status.HTTP_201_CREATED)
def create_invoice_image(
    image: image_schemas.InvoiceImageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new invoice image (requires authentication)"""
    return image_crud.create_invoice_image(db=db, image=image)


@router.get("/invoice/{invoice_id}", response_model=List[image_schemas.InvoiceImageResponse])
def list_invoice_images(
    invoice_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all images for an invoice (requires authentication)"""
    images = image_crud.get_invoice_images(db, invoice_id=invoice_id)
    return images


@router.get("/{image_id}", response_model=image_schemas.InvoiceImageResponse)
def get_invoice_image(
    image_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get an invoice image by ID (requires authentication)"""
    db_image = image_crud.get_invoice_image(db, image_id=image_id)
    if db_image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return db_image


@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_invoice_image(
    image_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete an invoice image (requires authentication)"""
    success = image_crud.delete_invoice_image(db, image_id=image_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return None


@router.delete("/invoice/{invoice_id}/all", status_code=status.HTTP_200_OK)
def delete_all_invoice_images(
    invoice_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete all images for an invoice (requires authentication)"""
    deleted_count = image_crud.delete_invoice_images(db, invoice_id=invoice_id)
    return {"deleted_count": deleted_count}
