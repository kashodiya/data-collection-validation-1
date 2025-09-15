

from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .base import BaseModel

class DataSubmission(BaseModel):
    """Model for tracking data submissions from financial institutions."""
    __tablename__ = "data_submissions"
    
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False, index=True)
    report_series_id = Column(Integer, ForeignKey("report_series.id"), nullable=False, index=True)
    reporting_date = Column(Date, nullable=False)
    submission_date = Column(DateTime, nullable=False)
    file_path = Column(String(255), nullable=False)
    status = Column(Enum('draft', 'submitted', 'validated', 'accepted', 'rejected', name='submission_status'), default='draft')
    validation_status = Column(Enum('pending', 'in_progress', 'passed', 'failed', 'warning', name='validation_status'), default='pending')
    
    # Relationships
    institution = relationship("Institution", backref="submissions")
    report_series = relationship("ReportSeries", backref="submissions")
    
    def __repr__(self):
        return f"<DataSubmission(id={self.id}, institution_id={self.institution_id}, report_series_id={self.report_series_id}, reporting_date='{self.reporting_date}')>"

