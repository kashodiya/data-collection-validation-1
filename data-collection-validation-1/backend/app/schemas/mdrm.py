





from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date

# Base MDRM schema with common attributes
class MDRMItemBase(BaseModel):
    mdrm_identifier: str = Field(..., description="MDRM identifier")
    item_name: str = Field(..., description="Item name")
    item_definition: Optional[str] = Field(None, description="Item definition")
    data_type: str = Field(..., description="Data type")
    valid_values: Optional[str] = Field(None, description="Valid values or ranges")
    series_mnemonic: Optional[str] = Field(None, description="Series mnemonic")
    effective_date: date = Field(..., description="Effective date")
    end_date: Optional[date] = Field(None, description="End date")

# Schema for creating a new MDRM item
class MDRMItemCreate(MDRMItemBase):
    pass

# Schema for updating an MDRM item
class MDRMItemUpdate(BaseModel):
    mdrm_identifier: Optional[str] = None
    item_name: Optional[str] = None
    item_definition: Optional[str] = None
    data_type: Optional[str] = None
    valid_values: Optional[str] = None
    series_mnemonic: Optional[str] = None
    effective_date: Optional[date] = None
    end_date: Optional[date] = None

# Schema for MDRM item response
class MDRMItemResponse(MDRMItemBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True





