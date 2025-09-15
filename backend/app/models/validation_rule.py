



from sqlalchemy import Column, String, Text, Date, Enum
from .base import BaseModel

class ValidationRule(BaseModel):
    """Model for defining validation rules for data submissions."""
    __tablename__ = "validation_rules"
    
    rule_name = Column(String(100), nullable=False)
    rule_description = Column(Text)
    rule_type = Column(Enum(
        'data_type', 
        'range', 
        'format', 
        'cross_field', 
        'historical', 
        'mathematical',
        name='rule_type'
    ), nullable=False)
    rule_definition = Column(Text, nullable=False)
    severity = Column(Enum('warning', 'error', name='rule_severity'), default='error')
    effective_date = Column(Date, nullable=False)
    end_date = Column(Date)
    
    def __repr__(self):
        return f"<ValidationRule(id={self.id}, rule_name='{self.rule_name}', rule_type='{self.rule_type}')>"



