














from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Base SubmittedData schema with common attributes
class SubmittedDataBase(BaseModel):
    submission_id: int = Field(..., description="Data submission ID")
    mdrm_identifier: str = Field(..., description="MDRM identifier")
    reported_value: str = Field(..., description="Reported value")
    calculated_value: Optional[str] = Field(None, description="Calculated value")

# Schema for creating new submitted data
class SubmittedDataCreate(SubmittedDataBase):
    pass

# Schema for updating submitted data
class SubmittedDataUpdate(BaseModel):
    submission_id: Optional[int] = None
    mdrm_identifier: Optional[str] = None
    reported_value: Optional[str] = None
    calculated_value: Optional[str] = None

# Schema for submitted data response
class SubmittedDataResponse(SubmittedDataBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True














