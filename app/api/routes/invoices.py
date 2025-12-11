from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
import os

from app.core.database import get_db
from app.core.deps import get_current_user
from app.schemas import invoice as invoice_schemas
from app.crud import invoice as invoice_crud
from app.models.user import User

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.post("/", response_model=invoice_schemas.InvoiceResponse, status_code=status.HTTP_201_CREATED)
def create_invoice(
    invoice: invoice_schemas.InvoiceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new invoice (auto-assigned to current user)"""
    return invoice_crud.create_invoice(db=db, invoice=invoice, user_id=current_user.id)


@router.get("/", response_model=List[invoice_schemas.InvoiceResponse])
def list_invoices(
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[uuid.UUID] = Query(None, description="Filter by user ID"),
    location_id: Optional[uuid.UUID] = Query(None, description="Filter by location ID"),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of invoices with optional filters (requires authentication)"""
    invoices = invoice_crud.get_invoices(
        db,
        skip=skip,
        limit=limit,
        user_id=user_id,
        location_id=location_id,
        category_id=category_id,
        status=status
    )
    return invoices


@router.get("/{invoice_id}", response_model=invoice_schemas.InvoiceWithImages)
def get_invoice(
    invoice_id: uuid.UUID,
    with_images: bool = Query(True, description="Include images in response"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get an invoice by ID (requires authentication)"""
    db_invoice = invoice_crud.get_invoice(db, invoice_id=invoice_id, with_images=with_images)
    if db_invoice is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    return db_invoice


@router.put("/{invoice_id}", response_model=invoice_schemas.InvoiceResponse)
def update_invoice(
    invoice_id: uuid.UUID,
    invoice: invoice_schemas.InvoiceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an invoice (requires authentication)"""
    db_invoice = invoice_crud.update_invoice(db, invoice_id=invoice_id, invoice=invoice)
    if db_invoice is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    return db_invoice


@router.delete("/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_invoice(
    invoice_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete an invoice (requires authentication)"""
    success = invoice_crud.delete_invoice(db, invoice_id=invoice_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    return None


    return invoices


@router.post("/{invoice_id}/images", status_code=status.HTTP_201_CREATED)
async def upload_invoice_image(
    invoice_id: uuid.UUID,
    file: UploadFile = File(...),
    gps_latitude: Optional[float] = Form(None),
    gps_longitude: Optional[float] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload an image for an invoice"""
    # Verify invoice exists and belongs to user (or admin)
    invoice = invoice_crud.get_invoice(db, invoice_id=invoice_id)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    
    if invoice.user_id != current_user.id and current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    # Save file to uploads directory organized by year/month
    from datetime import datetime
    now = datetime.now()
    upload_dir = os.path.join("uploads", str(now.year), f"{now.month:02d}")
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    file_ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(upload_dir, unique_filename)
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
        file_size = len(content)
    
    # Create database record
    image = invoice_crud.add_invoice_image(
        db=db,
        invoice_id=invoice_id,
        file_path=file_path,
        file_name=file.filename,
        file_size=file_size,
        mime_type=file.content_type,
        gps_latitude=gps_latitude,
        gps_longitude=gps_longitude
    )
    
    return image

