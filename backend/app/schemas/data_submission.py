











from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date

# Base DataSubmission schema with common attributes
class DataSubmissionBase(BaseModel):
    institution_id: int = Field(..., description="Institution ID")
    report_series_id: int = Field(..., description="Report series ID")
    reporting_date: date = Field(..., description="Reporting date")
    submission_date: datetime = Field(..., description="Submission date")
    file_path: str = Field(..., description="Path to submitted file")
    status: str = Field("draft", description="Submission status")
    validation_status: str = Field("pending", description="Validation status")

# Schema for creating a new data submission
class DataSubmissionCreate(DataSubmissionBase):
    pass

# Schema for updating a data submission
class DataSubmissionUpdate(BaseModel):
    institution_id: Optional[int] = None
    report_series_id: Optional[int] = None
    reporting_date: Optional[date] = None
    submission_date: Optional[datetime] = None
    file_path: Optional[str] = None
    status: Optional[str] = None
    validation_status: Optional[str] = None

# Schema for data submission response
class DataSubmissionResponse(DataSubmissionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True











