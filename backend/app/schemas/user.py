

























from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Base User schema with common attributes
class UserBase(BaseModel):
    username: str = Field(..., description="Username")
    email: str = Field(..., description="Email address")
    role: str = Field(..., description="User role")
    institution_id: Optional[int] = Field(None, description="Institution ID (for external users)")
    status: str = Field("active", description="User status")

# Schema for creating a new user
class UserCreate(UserBase):
    password: str = Field(..., description="Password")

# Schema for updating a user
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    institution_id: Optional[int] = None
    status: Optional[str] = None

# Schema for user response (without password)
class UserResponse(UserBase):
    id: int
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Token schemas for authentication
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

























