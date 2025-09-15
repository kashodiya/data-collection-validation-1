



























from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Response
from sqlalchemy.orm import Session
from datetime import datetime, date
import pandas as pd
import io

from ....core.database import get_db
from ....core.security import get_current_active_user, check_permissions
from ....models.data_submission import DataSubmission
from ....models.submitted_data import SubmittedData
from ....models.validation_result import ValidationResult
from ....models.institution import Institution
from ....models.user import User

router = APIRouter()

@router.get("/submissions/{submission_id}")
def generate_submission_report(
    submission_id: int,
    format: str = Query("csv", description="Report format (csv, excel, pdf)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Generate report for a submission.
    
    - External users can only generate reports for their own institution's submissions
    - Analysts and admins can generate reports for any submission
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
    
    # Get submitted data
    data_points = db.query(SubmittedData).filter(SubmittedData.submission_id == submission_id).all()
    
    # Create DataFrame
    df = pd.DataFrame([
        {
            "mdrm_identifier": data.mdrm_identifier,
            "reported_value": data.reported_value,
            "calculated_value": data.calculated_value
        }
        for data in data_points
    ])
    
    # Generate report based on format
    if format == "csv":
        # Generate CSV
        output = io.StringIO()
        df.to_csv(output, index=False)
        
        return Response(
            content=output.getvalue(),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=submission_{submission_id}_report.csv"}
        )
    
    elif format == "excel":
        # Generate Excel
        output = io.BytesIO()
        df.to_excel(output, index=False)
        
        return Response(
            content=output.getvalue(),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename=submission_{submission_id}_report.xlsx"}
        )
    
    elif format == "pdf":
        # In a real implementation, this would generate a PDF
        # For now, we'll just return an error
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="PDF generation not implemented"
        )
    
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid format. Supported formats: csv, excel, pdf"
        )

@router.get("/validation/{submission_id}")
def generate_validation_report(
    submission_id: int,
    format: str = Query("csv", description="Report format (csv, excel, pdf)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Generate validation report for a submission.
    
    - External users can only generate reports for their own institution's submissions
    - Analysts and admins can generate reports for any submission
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
    
    # Get validation results
    validation_results = db.query(ValidationResult).filter(ValidationResult.submission_id == submission_id).all()
    
    # Create DataFrame
    df = pd.DataFrame([
        {
            "field_identifier": result.field_identifier,
            "error_message": result.error_message,
            "severity": result.severity,
            "status": result.status
        }
        for result in validation_results
    ])
    
    # Generate report based on format
    if format == "csv":
        # Generate CSV
        output = io.StringIO()
        df.to_csv(output, index=False)
        
        return Response(
            content=output.getvalue(),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=validation_{submission_id}_report.csv"}
        )
    
    elif format == "excel":
        # Generate Excel
        output = io.BytesIO()
        df.to_excel(output, index=False)
        
        return Response(
            content=output.getvalue(),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename=validation_{submission_id}_report.xlsx"}
        )
    
    elif format == "pdf":
        # In a real implementation, this would generate a PDF
        # For now, we'll just return an error
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="PDF generation not implemented"
        )
    
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid format. Supported formats: csv, excel, pdf"
        )

@router.get("/historical/{institution_id}")
def generate_historical_report(
    institution_id: int,
    report_series_id: int = Query(..., description="Report series ID"),
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(..., description="End date (YYYY-MM-DD)"),
    format: str = Query("csv", description="Report format (csv, excel, pdf)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Generate historical report for an institution.
    
    - External users can only generate reports for their own institution
    - Analysts and admins can generate reports for any institution
    """
    # Check permissions
    if current_user.role == "external" and current_user.institution_id != institution_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Check if institution exists
    institution = db.query(Institution).filter(Institution.id == institution_id).first()
    if not institution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Institution with ID {institution_id} not found"
        )
    
    # Parse dates
    try:
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Use YYYY-MM-DD"
        )
    
    # Get submissions
    submissions = db.query(DataSubmission).filter(
        DataSubmission.institution_id == institution_id,
        DataSubmission.report_series_id == report_series_id,
        DataSubmission.reporting_date >= start_date_obj,
        DataSubmission.reporting_date <= end_date_obj
    ).all()
    
    # Create DataFrame
    data = []
    
    for submission in submissions:
        # Get submitted data
        data_points = db.query(SubmittedData).filter(SubmittedData.submission_id == submission.id).all()
        
        for data_point in data_points:
            data.append({
                "reporting_date": submission.reporting_date,
                "mdrm_identifier": data_point.mdrm_identifier,
                "reported_value": data_point.reported_value
            })
    
    df = pd.DataFrame(data)
    
    # Generate report based on format
    if format == "csv":
        # Generate CSV
        output = io.StringIO()
        df.to_csv(output, index=False)
        
        return Response(
            content=output.getvalue(),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=historical_{institution_id}_report.csv"}
        )
    
    elif format == "excel":
        # Generate Excel
        output = io.BytesIO()
        df.to_excel(output, index=False)
        
        return Response(
            content=output.getvalue(),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename=historical_{institution_id}_report.xlsx"}
        )
    
    elif format == "pdf":
        # In a real implementation, this would generate a PDF
        # For now, we'll just return an error
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="PDF generation not implemented"
        )
    
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid format. Supported formats: csv, excel, pdf"
        )



























