








from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ....core.database import get_db
from ....core.security import get_current_active_user, check_permissions
from ....models.institution import Institution
from ....models.user import User
from ....schemas.institution import InstitutionCreate, InstitutionUpdate, InstitutionResponse

router = APIRouter()

@router.get("/", response_model=List[InstitutionResponse])
def get_institutions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Retrieve institutions.
    
    - External users can only see their own institution
    - Analysts and admins can see all institutions
    """
    if current_user.role == "external" and current_user.institution_id:
        # External users can only see their own institution
        institutions = db.query(Institution).filter(
            Institution.id == current_user.institution_id
        ).offset(skip).limit(limit).all()
    else:
        # Analysts and admins can see all institutions
        institutions = db.query(Institution).offset(skip).limit(limit).all()
    
    return institutions

@router.post("/", response_model=InstitutionResponse, status_code=status.HTTP_201_CREATED)
def create_institution(
    institution_in: InstitutionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Create new institution.
    
    - Only analysts and admins can create institutions
    """
    # Check permissions
    if not check_permissions("analyst", current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Check if institution with same RSSD ID already exists
    db_institution = db.query(Institution).filter(
        Institution.rssd_id == institution_in.rssd_id
    ).first()
    
    if db_institution:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Institution with RSSD ID {institution_in.rssd_id} already exists"
        )
    
    # Create new institution
    institution = Institution(
        rssd_id=institution_in.rssd_id,
        name=institution_in.name,
        institution_type=institution_in.institution_type,
        contact_info=institution_in.contact_info,
        status=institution_in.status
    )
    
    db.add(institution)
    db.commit()
    db.refresh(institution)
    
    return institution

@router.get("/{institution_id}", response_model=InstitutionResponse)
def get_institution(
    institution_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get institution by ID.
    
    - External users can only see their own institution
    - Analysts and admins can see any institution
    """
    # Check if external user is trying to access another institution
    if current_user.role == "external" and current_user.institution_id != institution_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Get institution
    institution = db.query(Institution).filter(Institution.id == institution_id).first()
    
    if not institution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Institution with ID {institution_id} not found"
        )
    
    return institution

@router.put("/{institution_id}", response_model=InstitutionResponse)
def update_institution(
    institution_id: int,
    institution_in: InstitutionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Update institution.
    
    - External users can only update their own institution's contact info
    - Analysts and admins can update any institution
    """
    # Get institution
    institution = db.query(Institution).filter(Institution.id == institution_id).first()
    
    if not institution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Institution with ID {institution_id} not found"
        )
    
    # Check permissions
    if current_user.role == "external":
        # External users can only update their own institution's contact info
        if current_user.institution_id != institution_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        # External users can only update contact info
        if institution_in.contact_info is not None:
            institution.contact_info = institution_in.contact_info
    else:
        # Analysts and admins can update any field
        update_data = institution_in.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(institution, field, value)
    
    db.commit()
    db.refresh(institution)
    
    return institution

@router.delete("/{institution_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_institution(
    institution_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> None:
    """
    Delete institution.
    
    - Only admins can delete institutions
    """
    # Check permissions
    if not check_permissions("admin", current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Get institution
    institution = db.query(Institution).filter(Institution.id == institution_id).first()
    
    if not institution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Institution with ID {institution_id} not found"
        )
    
    # Delete institution
    db.delete(institution)
    db.commit()








