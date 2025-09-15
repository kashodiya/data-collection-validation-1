

from sqlalchemy import Column, String, Text, Enum
from .base import BaseModel

class ReportSeries(BaseModel):
    """Model for report series (e.g., FR Y-9C, FFIEC 031, etc.)."""
    __tablename__ = "report_series"
    
    series_code = Column(String(20), unique=True, nullable=False, index=True)
    series_name = Column(String(255), nullable=False)
    description = Column(Text)
    filing_frequency = Column(Enum('monthly', 'quarterly', 'annual', 'ad_hoc', name='filing_frequency'), nullable=False)
    form_pdf_path = Column(String(255))
    instructions_pdf_path = Column(String(255))
    status = Column(Enum('active', 'inactive', name='report_series_status'), default='active')
    
    def __repr__(self):
        return f"<ReportSeries(id={self.id}, series_code='{self.series_code}', series_name='{self.series_name}')>"

