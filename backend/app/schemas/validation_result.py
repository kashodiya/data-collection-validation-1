





















from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Base ValidationResult schema with common attributes
class ValidationResultBase(BaseModel):
    submission_id: int = Field(..., description="Data submission ID")
    rule_id: int = Field(..., description="Validation rule ID")
    field_identifier: str = Field(..., description="Field identifier (MDRM)")
    error_message: str = Field(..., description="Error message")
    severity: str = Field("error", description="Result severity")
    status: str = Field("open", description="Result status")
    resolved_at: Optional[datetime] = Field(None, description="Resolution timestamp")

# Schema for creating a new validation result
class ValidationResultCreate(ValidationResultBase):
    pass

# Schema for updating a validation result
class ValidationResultUpdate(BaseModel):
    submission_id: Optional[int] = None
    rule_id: Optional[int] = None
    field_identifier: Optional[str] = None
    error_message: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[str] = None
    resolved_at: Optional[datetime] = None

# Schema for validation result response
class ValidationResultResponse(ValidationResultBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True





















