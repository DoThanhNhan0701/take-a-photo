from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
import os

from app.core.database import get_db
from app.core.deps import get_current_user
from app.schemas import invoice as invoice_schemas
from app.crud import invoice as invoice_crud
from app.crud import location as location_crud
from app.models.user import User

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_invoice(
    location_id: Optional[uuid.UUID] = Form(None),
    category_id: Optional[int] = Form(None),
    note: Optional[str] = Form(None),
    status: str = Form("draft"),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new invoice with an image (auto-assigned to current user)"""
    # 1. Create Invoice
    # Get GPS from location if provided
    gps_latitude = None
    gps_longitude = None
    
    if location_id:
        location = location_crud.get_location(db, location_id=location_id)
        if location:
            gps_latitude = float(location.gps_latitude) if location.gps_latitude is not None else None
            gps_longitude = float(location.gps_longitude) if location.gps_longitude is not None else None

    # Add GPS to extra_metadata if provided
    extra_metadata = {}
    if gps_latitude is not None:
        extra_metadata["gps_latitude"] = gps_latitude
    if gps_longitude is not None:
        extra_metadata["gps_longitude"] = gps_longitude
        
    invoice_data = invoice_schemas.InvoiceCreate(
        location_id=location_id,
        category_id=category_id,
        note=note,
        status=status,
        extra_metadata=extra_metadata
    )
    db_invoice = invoice_crud.create_invoice(db=db, invoice=invoice_data, user_id=current_user.id)
    
    # 2. Save Image
    try:
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
        
        # 3. Create Image Record
        invoice_crud.add_invoice_image(
            db=db,
            invoice_id=db_invoice.id,
            file_path=file_path,
            file_name=file.filename,
            file_size=file_size,
            mime_type=file.content_type,
            gps_latitude=gps_latitude,
            gps_longitude=gps_longitude
        )
        
        # Refresh invoice to include images
        db.refresh(db_invoice)
        
        # Validate model to ensure structure is correct
        validated = invoice_schemas.InvoiceWithImages.model_validate(db_invoice)
        return validated.model_dump()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating invoice: {str(e)}")



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





