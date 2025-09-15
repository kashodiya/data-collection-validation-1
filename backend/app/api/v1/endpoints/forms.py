






























from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File, Form, Response
from sqlalchemy.orm import Session
import os
from datetime import datetime

from ....core.database import get_db
from ....core.security import get_current_active_user, check_permissions
from ....core.config import settings
from ....models.report_series import ReportSeries
from ....models.user import User

router = APIRouter()

@router.get("/")
def list_forms(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    List available forms.
    """
    # Get all active report series
    report_series = db.query(ReportSeries).filter(ReportSeries.status == "active").all()
    
    # Create response
    forms = []
    for series in report_series:
        forms.append({
            "id": series.id,
            "series_code": series.series_code,
            "series_name": series.series_name,
            "has_form": bool(series.form_pdf_path),
            "has_instructions": bool(series.instructions_pdf_path)
        })
    
    return forms

@router.get("/{series_id}")
def get_form(
    series_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get form for report series.
    """
    # Get report series
    series = db.query(ReportSeries).filter(ReportSeries.id == series_id).first()
    
    if not series:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report series with ID {series_id} not found"
        )
    
    if not series.form_pdf_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No form available for report series {series.series_code}"
        )
    
    # Check if file exists
    if not os.path.isfile(series.form_pdf_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Form file not found for report series {series.series_code}"
        )
    
    # Read file
    with open(series.form_pdf_path, "rb") as f:
        file_content = f.read()
    
    # Return file
    return Response(
        content=file_content,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={series.series_code}_form.pdf"}
    )

@router.get("/instructions/{series_id}")
def get_instructions(
    series_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get instructions for report series.
    """
    # Get report series
    series = db.query(ReportSeries).filter(ReportSeries.id == series_id).first()
    
    if not series:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report series with ID {series_id} not found"
        )
    
    if not series.instructions_pdf_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No instructions available for report series {series.series_code}"
        )
    
    # Check if file exists
    if not os.path.isfile(series.instructions_pdf_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Instructions file not found for report series {series.series_code}"
        )
    
    # Read file
    with open(series.instructions_pdf_path, "rb") as f:
        file_content = f.read()
    
    # Return file
    return Response(
        content=file_content,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={series.series_code}_instructions.pdf"}
    )

@router.post("/upload/{series_id}/form", status_code=status.HTTP_201_CREATED)
async def upload_form(
    series_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Upload form for report series.
    
    - Only analysts and admins can upload forms
    """
    # Check permissions
    if not check_permissions("analyst", current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Get report series
    series = db.query(ReportSeries).filter(ReportSeries.id == series_id).first()
    
    if not series:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report series with ID {series_id} not found"
        )
    
    # Check file extension
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported"
        )
    
    # Create forms directory if it doesn't exist
    forms_dir = os.path.join(settings.UPLOAD_DIR, "forms")
    os.makedirs(forms_dir, exist_ok=True)
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{series.series_code}_form_{timestamp}.pdf"
    file_path = os.path.join(forms_dir, filename)
    
    # Save file
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # Update report series
    series.form_pdf_path = file_path
    db.commit()
    
    return {
        "detail": "Form uploaded successfully",
        "series_code": series.series_code,
        "form_path": file_path
    }

@router.post("/upload/{series_id}/instructions", status_code=status.HTTP_201_CREATED)
async def upload_instructions(
    series_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Upload instructions for report series.
    
    - Only analysts and admins can upload instructions
    """
    # Check permissions
    if not check_permissions("analyst", current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Get report series
    series = db.query(ReportSeries).filter(ReportSeries.id == series_id).first()
    
    if not series:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report series with ID {series_id} not found"
        )
    
    # Check file extension
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported"
        )
    
    # Create forms directory if it doesn't exist
    forms_dir = os.path.join(settings.UPLOAD_DIR, "forms")
    os.makedirs(forms_dir, exist_ok=True)
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{series.series_code}_instructions_{timestamp}.pdf"
    file_path = os.path.join(forms_dir, filename)
    
    # Save file
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # Update report series
    series.instructions_pdf_path = file_path
    db.commit()
    
    return {
        "detail": "Instructions uploaded successfully",
        "series_code": series.series_code,
        "instructions_path": file_path
    }






























