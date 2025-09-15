




import os
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class Settings(BaseModel):
    """Application settings."""
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Federal Reserve Data Collection System"
    
    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "YOUR_SECRET_KEY_HERE")  # In production, use environment variable
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./frb_data_collection.db")
    
    # File storage settings
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100 MB
    ALLOWED_EXTENSIONS: List[str] = ["csv", "xlsx", "xls", "xml", "json"]
    
    # CORS settings
    CORS_ORIGINS: List[str] = ["*"]  # In production, restrict to specific origins
    
    # Logging settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    class Config:
        case_sensitive = True

# Create settings instance
settings = Settings()




