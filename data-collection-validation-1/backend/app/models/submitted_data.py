


from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class SubmittedData(BaseModel):
    """Model for storing the actual data values submitted by institutions."""
    __tablename__ = "submitted_data"
    
    submission_id = Column(Integer, ForeignKey("data_submissions.id"), nullable=False, index=True)
    mdrm_identifier = Column(String(20), nullable=False, index=True)
    reported_value = Column(Text, nullable=False)
    calculated_value = Column(Text)
    
    # Relationships
    submission = relationship("DataSubmission", backref="data_points")
    
    def __repr__(self):
        return f"<SubmittedData(id={self.id}, submission_id={self.submission_id}, mdrm_identifier='{self.mdrm_identifier}')>"


