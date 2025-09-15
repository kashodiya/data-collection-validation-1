

















from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date

# Base ValidationRule schema with common attributes
class ValidationRuleBase(BaseModel):
    rule_name: str = Field(..., description="Rule name")
    rule_description: Optional[str] = Field(None, description="Rule description")
    rule_type: str = Field(..., description="Rule type")
    rule_definition: str = Field(..., description="Rule definition")
    severity: str = Field("error", description="Rule severity")
    effective_date: date = Field(..., description="Effective date")
    end_date: Optional[date] = Field(None, description="End date")

# Schema for creating a new validation rule
class ValidationRuleCreate(ValidationRuleBase):
    pass

# Schema for updating a validation rule
class ValidationRuleUpdate(BaseModel):
    rule_name: Optional[str] = None
    rule_description: Optional[str] = None
    rule_type: Optional[str] = None
    rule_definition: Optional[str] = None
    severity: Optional[str] = None
    effective_date: Optional[date] = None
    end_date: Optional[date] = None

# Schema for validation rule response
class ValidationRuleResponse(ValidationRuleBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

















