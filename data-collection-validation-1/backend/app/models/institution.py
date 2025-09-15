
from sqlalchemy import Column, String, Integer, Text, Enum
from .base import BaseModel

class Institution(BaseModel):
    """Model for financial institutions."""
    __tablename__ = "institutions"
    
    rssd_id = Column(String(10), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    institution_type = Column(String(50), nullable=False)
    contact_info = Column(Text)
    status = Column(Enum('active', 'inactive', name='institution_status'), default='active')
    
    def __repr__(self):
        return f"<Institution(id={self.id}, name='{self.name}', rssd_id='{self.rssd_id}')>"
