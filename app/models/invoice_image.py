import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class InvoiceImage(Base):
    """Invoice image model for captured photos"""
    
    __tablename__ = "invoice_images"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    invoice_id = Column(UUID(as_uuid=True), ForeignKey('invoices.id', ondelete='CASCADE'), nullable=False)
    
    file_path = Column(Text, nullable=False)  # S3/MinIO path
    file_name = Column(String(255))
    file_size = Column(Integer)  # Size in bytes
    mime_type = Column(String(50))  # image/jpeg, image/png
    
    # GPS coordinates from photo capture
    gps_latitude = Column(Numeric(9, 6))
    gps_longitude = Column(Numeric(9, 6))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    invoice = relationship("Invoice", back_populates="images")
    
    def __repr__(self):
        return f"<InvoiceImage(id='{self.id}', file_name='{self.file_name}')>"
