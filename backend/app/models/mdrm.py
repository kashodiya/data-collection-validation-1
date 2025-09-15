
from sqlalchemy import Column, String, Text, Date
from .base import BaseModel

class MDRMItem(BaseModel):
    """Model for MDRM (Micro Data Reference Manual) data elements."""
    __tablename__ = "mdrm_items"
    
    mdrm_identifier = Column(String(20), unique=True, nullable=False, index=True)
    item_name = Column(String(255), nullable=False)
    item_definition = Column(Text)
    data_type = Column(String(50), nullable=False)
    valid_values = Column(Text)
    series_mnemonic = Column(String(50), index=True)
    effective_date = Column(Date, nullable=False)
    end_date = Column(Date)
    
    def __repr__(self):
        return f"<MDRMItem(id={self.id}, mdrm_identifier='{self.mdrm_identifier}', item_name='{self.item_name}')>"
