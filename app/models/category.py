from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


class Category(Base):
    """Category model for invoice types"""
    
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    code = Column(String(50), unique=True, index=True)
    icon_name = Column(String(50))  # Icon identifier for mobile app
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    invoices = relationship("Invoice", back_populates="category")
    
    def __repr__(self):
        return f"<Category(name='{self.name}', code='{self.code}')>"
