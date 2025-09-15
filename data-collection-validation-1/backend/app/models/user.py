






from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from .base import BaseModel

class User(BaseModel):
    """Model for user authentication and authorization."""
    __tablename__ = "users"
    
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    role = Column(Enum('external', 'analyst', 'admin', name='user_role'), nullable=False)
    institution_id = Column(Integer, ForeignKey("institutions.id"))
    status = Column(Enum('active', 'inactive', 'locked', name='user_status'), default='active')
    last_login = Column(DateTime)
    
    # Relationships
    institution = relationship("Institution", backref="users")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"






