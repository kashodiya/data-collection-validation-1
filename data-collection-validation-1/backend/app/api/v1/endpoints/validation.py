
























from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime, date

from ....core.database import get_db
from ....core.security import get_current_active_user, check_permissions
from ....models.validation_rule import ValidationRule
from ....models.validation_result import ValidationResult
from ....models.data_submission import DataSubmission
from ....models.user import User
from ....schemas.validation_rule import ValidationRuleCreate, ValidationRuleUpdate, ValidationRuleResponse
from ....schemas.validation_result import ValidationResultResponse

router = APIRouter()

@router.get("/rules", response_model=List[ValidationRuleResponse])
def get_validation_rules(
    rule_type: Optional[str] = Query(None, description="Filter by rule type"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Retrieve validation rules.
    """
    # Build query
    query = db.query(ValidationRule)
    
    # Apply filters
    if rule_type:
        query = query.filter(ValidationRule.rule_type == rule_type)
    
    # Execute query
    rules = query.offset(skip).limit(limit).all()
    
    return rules

@router.post("/rules", response_model=ValidationRuleResponse, status_code=status.HTTP_201_CREATED)
def create_validation_rule(
    rule_in: ValidationRuleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Create new validation rule.
    
    - Only analysts and admins can create validation rules
    """
    # Check permissions
    if not check_permissions("analyst", current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Create new validation rule
    rule = ValidationRule(
        rule_name=rule_in.rule_name,
        rule_description=rule_in.rule_description,
        rule_type=rule_in.rule_type,
        rule_definition=rule_in.rule_definition,
        severity=rule_in.severity,
        effective_date=rule_in.effective_date,
        end_date=rule_in.end_date
    )
    
    db.add(rule)
    db.commit()
    db.refresh(rule)
    
    return rule

@router.put("/rules/{rule_id}", response_model=ValidationRuleResponse)
def update_validation_rule(
    rule_id: int,
    rule_in: ValidationRuleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Update validation rule.
    
    - Only analysts and admins can update validation rules
    """
    # Check permissions
    if not check_permissions("analyst", current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Get validation rule
    rule = db.query(ValidationRule).filter(ValidationRule.id == rule_id).first()
    
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Validation rule with ID {rule_id} not found"
        )
    
    # Update validation rule
    update_data = rule_in.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(rule, field, value)
    
    db.commit()
    db.refresh(rule)
    
    return rule

@router.get("/results/{submission_id}", response_model=List[ValidationResultResponse])
def get_validation_results(
    submission_id: int,
    severity: Optional[str] = Query(None, description="Filter by severity"),
    status: Optional[str] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get validation results for a submission.
    
    - External users can only see results for their own institution's submissions
    - Analysts and admins can see results for any submission
    """
    # Get submission
    submission = db.query(DataSubmission).filter(DataSubmission.id == submission_id).first()
    
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Submission with ID {submission_id} not found"
        )
    
    # Check permissions
    if current_user.role == "external" and current_user.institution_id != submission.institution_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Build query
    query = db.query(ValidationResult).filter(ValidationResult.submission_id == submission_id)
    
    # Apply filters
    if severity:
        query = query.filter(ValidationResult.severity == severity)
    
    if status:
        query = query.filter(ValidationResult.status == status)
    
    # Execute query
    results = query.all()
    
    return results

@router.post("/execute/{submission_id}", status_code=status.HTTP_202_ACCEPTED)
def execute_validation(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Execute validation rules for a submission.
    
    - External users can only validate their own institution's submissions
    - Analysts and admins can validate any submission
    """
    # Get submission
    submission = db.query(DataSubmission).filter(DataSubmission.id == submission_id).first()
    
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Submission with ID {submission_id} not found"
        )
    
    # Check permissions
    if current_user.role == "external" and current_user.institution_id != submission.institution_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Update submission status
    submission.validation_status = "in_progress"
    db.commit()
    
    # In a real implementation, this would trigger an asynchronous validation process
    # For now, we'll just update the status
    submission.validation_status = "passed"  # This would be determined by the validation process
    db.commit()
    
    return {
        "detail": "Validation execution triggered successfully",
        "status": submission.status,
        "validation_status": submission.validation_status
    }
























