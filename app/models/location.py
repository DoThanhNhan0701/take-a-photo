import uuid
from sqlalchemy import Column, String, Text, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Location(Base):
    """Location model for stores/supermarkets"""
    
    __tablename__ = "locations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    address = Column(Text)
    code = Column(String(50), unique=True, index=True)
    # GPS coordinates as decimal values
    gps_latitude = Column(Numeric(9, 6))  # -90 to 90
    gps_longitude = Column(Numeric(9, 6))  # -180 to 180
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    invoices = relationship("Invoice", back_populates="location")
    
    def __repr__(self):
        return f"<Location(name='{self.name}', code='{self.code}')>"
