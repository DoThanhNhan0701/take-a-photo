from sqlalchemy.orm import Session, joinedload
from typing import Optional
import uuid

from app.models.invoice import Invoice
from app.schemas.invoice import InvoiceCreate, InvoiceUpdate


def get_invoice(db: Session, invoice_id: uuid.UUID, with_images: bool = False) -> Optional[Invoice]:
    """Get an invoice by ID"""
    query = db.query(Invoice)
    if with_images:
        query = query.options(joinedload(Invoice.images))
    return query.filter(Invoice.id == invoice_id).first()


def get_invoices(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[uuid.UUID] = None,
    location_id: Optional[uuid.UUID] = None,
    category_id: Optional[int] = None,
    status: Optional[str] = None
) -> list[Invoice]:
    """Get all invoices with filtering and pagination"""
    query = db.query(Invoice)
    
    if user_id:
        query = query.filter(Invoice.user_id == user_id)
    if location_id:
        query = query.filter(Invoice.location_id == location_id)
    if category_id:
        query = query.filter(Invoice.category_id == category_id)
    if status:
        query = query.filter(Invoice.status == status)
    
    return query.order_by(Invoice.captured_at.desc()).offset(skip).limit(limit).all()


def create_invoice(db: Session, invoice: InvoiceCreate, user_id: uuid.UUID) -> Invoice:
    """Create a new invoice"""
    db_invoice = Invoice(
        user_id=user_id,
        location_id=invoice.location_id,
        category_id=invoice.category_id,
        status=invoice.status.value,
        note=invoice.note,
        extra_metadata=invoice.extra_metadata
    )
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice


def update_invoice(db: Session, invoice_id: uuid.UUID, invoice: InvoiceUpdate) -> Optional[Invoice]:
    """Update an invoice"""
    db_invoice = get_invoice(db, invoice_id)
    if not db_invoice:
        return None
    
    update_data = invoice.model_dump(exclude_unset=True)
    
    # Convert status enum to string if present
    if 'status' in update_data and update_data['status']:
        update_data['status'] = update_data['status'].value
    
    for field, value in update_data.items():
        setattr(db_invoice, field, value)
    
    db.commit()
    db.refresh(db_invoice)
    return db_invoice


def delete_invoice(db: Session, invoice_id: uuid.UUID) -> bool:
    """Delete an invoice"""
    db_invoice = get_invoice(db, invoice_id)
    if not db_invoice:
        return False
    
    db.delete(db_invoice)
    db.commit()
    return True


from app.models.invoice_image import InvoiceImage

def get_user_invoices_by_status(db: Session, user_id: uuid.UUID, status: str) -> list[Invoice]:
    """Get all invoices for a user with a specific status"""
    return db.query(Invoice).filter(
        Invoice.user_id == user_id,
        Invoice.status == status
    ).order_by(Invoice.captured_at.desc()).all()


def add_invoice_image(
    db: Session,
    invoice_id: uuid.UUID,
    file_path: str,
    file_name: str,
    file_size: int,
    mime_type: str,
    gps_latitude: Optional[float] = None,
    gps_longitude: Optional[float] = None
) -> InvoiceImage:
    """Add an image to an invoice"""
    db_image = InvoiceImage(
        invoice_id=invoice_id,
        file_path=file_path,
        file_name=file_name,
        file_size=file_size,
        mime_type=mime_type,
        gps_latitude=gps_latitude,
        gps_longitude=gps_longitude
    )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

