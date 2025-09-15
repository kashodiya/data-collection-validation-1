















from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ....core.database import get_db
from ....core.security import get_current_active_user, check_permissions
from ....models.report_series import ReportSeries
from ....models.user import User
from ....schemas.report_series import ReportSeriesCreate, ReportSeriesUpdate, ReportSeriesResponse

router = APIRouter()

@router.get("/", response_model=List[ReportSeriesResponse])
def get_report_series(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Retrieve report series.
    """
    report_series = db.query(ReportSeries).offset(skip).limit(limit).all()
    return report_series

@router.post("/", response_model=ReportSeriesResponse, status_code=status.HTTP_201_CREATED)
def create_report_series(
    report_series_in: ReportSeriesCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Create new report series.
    
    - Only analysts and admins can create report series
    """
    # Check permissions
    if not check_permissions("analyst", current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Check if report series with same code already exists
    db_report_series = db.query(ReportSeries).filter(
        ReportSeries.series_code == report_series_in.series_code
    ).first()
    
    if db_report_series:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Report series with code {report_series_in.series_code} already exists"
        )
    
    # Create new report series
    report_series = ReportSeries(
        series_code=report_series_in.series_code,
        series_name=report_series_in.series_name,
        description=report_series_in.description,
        filing_frequency=report_series_in.filing_frequency,
        form_pdf_path=report_series_in.form_pdf_path,
        instructions_pdf_path=report_series_in.instructions_pdf_path,
        status=report_series_in.status
    )
    
    db.add(report_series)
    db.commit()
    db.refresh(report_series)
    
    return report_series

@router.get("/{report_series_id}", response_model=ReportSeriesResponse)
def get_report_series_by_id(
    report_series_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get report series by ID.
    """
    report_series = db.query(ReportSeries).filter(ReportSeries.id == report_series_id).first()
    
    if not report_series:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report series with ID {report_series_id} not found"
        )
    
    return report_series

@router.put("/{report_series_id}", response_model=ReportSeriesResponse)
def update_report_series(
    report_series_id: int,
    report_series_in: ReportSeriesUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Update report series.
    
    - Only analysts and admins can update report series
    """
    # Check permissions
    if not check_permissions("analyst", current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Get report series
    report_series = db.query(ReportSeries).filter(ReportSeries.id == report_series_id).first()
    
    if not report_series:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report series with ID {report_series_id} not found"
        )
    
    # Update report series
    update_data = report_series_in.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(report_series, field, value)
    
    db.commit()
    db.refresh(report_series)
    
    return report_series

@router.delete("/{report_series_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_report_series(
    report_series_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> None:
    """
    Delete report series.
    
    - Only admins can delete report series
    """
    # Check permissions
    if not check_permissions("admin", current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Get report series
    report_series = db.query(ReportSeries).filter(ReportSeries.id == report_series_id).first()
    
    if not report_series:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report series with ID {report_series_id} not found"
        )
    
    # Delete report series
    db.delete(report_series)
    db.commit()















