from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

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


@router.get("/user/{user_id}/status/{status}", response_model=List[invoice_schemas.InvoiceResponse])
def get_user_invoices_by_status(
    user_id: uuid.UUID,
    status: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all invoices for a user with a specific status (requires authentication)"""
    invoices = invoice_crud.get_user_invoices_by_status(db, user_id=user_id, status=status)
    return invoices
