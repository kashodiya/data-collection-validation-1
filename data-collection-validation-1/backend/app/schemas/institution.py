



from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Base Institution schema with common attributes
class InstitutionBase(BaseModel):
    rssd_id: str = Field(..., description="Institution RSSD ID")
    name: str = Field(..., description="Institution name")
    institution_type: str = Field(..., description="Type of financial institution")
    contact_info: Optional[str] = Field(None, description="Contact information")
    status: str = Field("active", description="Institution status")

# Schema for creating a new institution
class InstitutionCreate(InstitutionBase):
    pass

# Schema for updating an institution
class InstitutionUpdate(BaseModel):
    rssd_id: Optional[str] = None
    name: Optional[str] = None
    institution_type: Optional[str] = None
    contact_info: Optional[str] = None
    status: Optional[str] = None

# Schema for institution response
class InstitutionResponse(InstitutionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True



