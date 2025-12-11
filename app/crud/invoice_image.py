from sqlalchemy.orm import Session
from typing import Optional
import uuid

from app.models.invoice_image import InvoiceImage
from app.schemas.invoice_image import InvoiceImageCreate


def get_invoice_image(db: Session, image_id: uuid.UUID) -> Optional[InvoiceImage]:
    """Get an invoice image by ID"""
    return db.query(InvoiceImage).filter(InvoiceImage.id == image_id).first()


def get_invoice_images(db: Session, invoice_id: uuid.UUID) -> list[InvoiceImage]:
    """Get all images for an invoice"""
    return db.query(InvoiceImage).filter(
        InvoiceImage.invoice_id == invoice_id
    ).order_by(InvoiceImage.created_at).all()


def create_invoice_image(db: Session, image: InvoiceImageCreate) -> InvoiceImage:
    """Create a new invoice image"""
    db_image = InvoiceImage(
        invoice_id=image.invoice_id,
        file_path=image.file_path,
        file_name=image.file_name,
        file_size=image.file_size,
        mime_type=image.mime_type,
        gps_latitude=image.gps_latitude,
        gps_longitude=image.gps_longitude
    )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def delete_invoice_image(db: Session, image_id: uuid.UUID) -> bool:
    """Delete an invoice image"""
    db_image = get_invoice_image(db, image_id)
    if not db_image:
        return False
    
    db.delete(db_image)
    db.commit()
    return True


def delete_invoice_images(db: Session, invoice_id: uuid.UUID) -> int:
    """Delete all images for an invoice"""
    deleted_count = db.query(InvoiceImage).filter(
        InvoiceImage.invoice_id == invoice_id
    ).delete()
    db.commit()
    return deleted_count
