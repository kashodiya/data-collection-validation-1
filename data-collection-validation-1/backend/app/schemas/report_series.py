








from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Base ReportSeries schema with common attributes
class ReportSeriesBase(BaseModel):
    series_code: str = Field(..., description="Report series code")
    series_name: str = Field(..., description="Report series name")
    description: Optional[str] = Field(None, description="Report series description")
    filing_frequency: str = Field(..., description="Filing frequency")
    form_pdf_path: Optional[str] = Field(None, description="Path to form PDF")
    instructions_pdf_path: Optional[str] = Field(None, description="Path to instructions PDF")
    status: str = Field("active", description="Report series status")

# Schema for creating a new report series
class ReportSeriesCreate(ReportSeriesBase):
    pass

# Schema for updating a report series
class ReportSeriesUpdate(BaseModel):
    series_code: Optional[str] = None
    series_name: Optional[str] = None
    description: Optional[str] = None
    filing_frequency: Optional[str] = None
    form_pdf_path: Optional[str] = None
    instructions_pdf_path: Optional[str] = None
    status: Optional[str] = None

# Schema for report series response
class ReportSeriesResponse(ReportSeriesBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True








