from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TimestampMixin:
    """Mixin for adding created_at and updated_at columns to models."""
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

class BaseModel(Base, TimestampMixin):
    """Base model class with common fields and methods."""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)
