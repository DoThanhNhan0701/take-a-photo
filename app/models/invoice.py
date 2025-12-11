import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Invoice(Base):
    """Invoice model for photo capture sessions"""
    
    __tablename__ = "invoices"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    location_id = Column(UUID(as_uuid=True), ForeignKey('locations.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    
    status = Column(String(20), default='draft')  # draft, completed, synced
    note = Column(Text)
    extra_metadata = Column(JSONB, default={})  # Additional metadata like "Biên bản", "KTSSS"
    
    captured_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="invoices")
    location = relationship("Location", back_populates="invoices")
    category = relationship("Category", back_populates="invoices")
    images = relationship("InvoiceImage", back_populates="invoice", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Invoice(id='{self.id}', status='{self.status}')>"
