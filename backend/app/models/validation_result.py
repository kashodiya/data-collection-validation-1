




from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from .base import BaseModel

class ValidationResult(BaseModel):
    """Model for storing validation results for data submissions."""
    __tablename__ = "validation_results"
    
    submission_id = Column(Integer, ForeignKey("data_submissions.id"), nullable=False, index=True)
    rule_id = Column(Integer, ForeignKey("validation_rules.id"), nullable=False)
    field_identifier = Column(String(20), nullable=False)  # MDRM identifier
    error_message = Column(Text, nullable=False)
    severity = Column(Enum('warning', 'error', name='result_severity'), default='error')
    status = Column(Enum('open', 'resolved', 'waived', name='result_status'), default='open')
    resolved_at = Column(DateTime)
    
    # Relationships
    submission = relationship("DataSubmission", backref="validation_results")
    rule = relationship("ValidationRule")
    
    def __repr__(self):
        return f"<ValidationResult(id={self.id}, submission_id={self.submission_id}, field_identifier='{self.field_identifier}', severity='{self.severity}')>"




