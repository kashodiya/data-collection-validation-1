


















from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
import os
import pandas as pd
import json
import xml.etree.ElementTree as ET
from datetime import datetime, date

from ....core.database import get_db
from ....core.security import get_current_active_user, check_permissions
from ....core.config import settings
from ....models.data_submission import DataSubmission
from ....models.submitted_data import SubmittedData
from ....models.institution import Institution
from ....models.report_series import ReportSeries
from ....models.user import User
from ....schemas.data_submission import DataSubmissionCreate, DataSubmissionUpdate, DataSubmissionResponse

router = APIRouter()

@router.get("/", response_model=List[DataSubmissionResponse])
def get_submissions(
    institution_id: Optional[int] = Query(None, description="Filter by institution ID"),
    report_series_id: Optional[int] = Query(None, description="Filter by report series ID"),
    status: Optional[str] = Query(None, description="Filter by submission status"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Retrieve data submissions.
    
    - External users can only see their own institution's submissions
    - Analysts and admins can see all submissions
    """
    # Build query
    query = db.query(DataSubmission)
    
    # Apply filters
    if institution_id:
        query = query.filter(DataSubmission.institution_id == institution_id)
    
    if report_series_id:
        query = query.filter(DataSubmission.report_series_id == report_series_id)
    
    if status:
        query = query.filter(DataSubmission.status == status)
    
    # Apply permission-based filters
    if current_user.role == "external" and current_user.institution_id:
        query = query.filter(DataSubmission.institution_id == current_user.institution_id)
    
    # Execute query
    submissions = query.offset(skip).limit(limit).all()
    
    return submissions

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_submission(
    institution_id: int = Form(...),
    report_series_id: int = Form(...),
    reporting_date: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Upload data submission file.
    
    - External users can only upload for their own institution
    - Analysts and admins can upload for any institution
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
    
    # Check if report series exists
    report_series = db.query(ReportSeries).filter(ReportSeries.id == report_series_id).first()
    if not report_series:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report series with ID {report_series_id} not found"
        )
    
    # Parse reporting date
    try:
        reporting_date_obj = datetime.strptime(reporting_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid reporting date format. Use YYYY-MM-DD"
        )
    
    # Check file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ['.csv', '.xlsx', '.xls', '.xml', '.json']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file format. Supported formats: CSV, Excel, XML, JSON"
        )
    
    # Create upload directory if it doesn't exist
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{institution.rssd_id}_{report_series.series_code}_{reporting_date}_{timestamp}{file_ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, filename)
    
    # Save file
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # Create submission record
    submission = DataSubmission(
        institution_id=institution_id,
        report_series_id=report_series_id,
        reporting_date=reporting_date_obj,
        submission_date=datetime.now(),
        file_path=file_path,
        status="submitted",
        validation_status="pending"
    )
    
    db.add(submission)
    db.commit()
    db.refresh(submission)
    
    # Process file and extract data
    try:
        await process_submission_file(submission.id, file_path, file_ext, db)
    except Exception as e:
        # Update submission status on error
        submission.status = "draft"
        submission.validation_status = "failed"
        db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing submission file: {str(e)}"
        )
    
    return {
        "id": submission.id,
        "detail": "Submission uploaded successfully",
        "status": submission.status,
        "validation_status": submission.validation_status
    }

@router.get("/{submission_id}", response_model=DataSubmissionResponse)
def get_submission(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get submission by ID.
    
    - External users can only see their own institution's submissions
    - Analysts and admins can see any submission
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
    
    return submission

@router.post("/{submission_id}/validate", status_code=status.HTTP_202_ACCEPTED)
def validate_submission(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Trigger validation for a submission.
    
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
        "detail": "Validation triggered successfully",
        "status": submission.status,
        "validation_status": submission.validation_status
    }

@router.put("/{submission_id}/status", response_model=DataSubmissionResponse)
def update_submission_status(
    submission_id: int,
    status: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Update submission status.
    
    - External users can only update their own institution's submissions
    - Analysts and admins can update any submission
    """
    # Check if status is valid
    valid_statuses = ["draft", "submitted", "validated", "accepted", "rejected"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Valid statuses: {', '.join(valid_statuses)}"
        )
    
    # Get submission
    submission = db.query(DataSubmission).filter(DataSubmission.id == submission_id).first()
    
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Submission with ID {submission_id} not found"
        )
    
    # Check permissions
    if current_user.role == "external":
        # External users can only update their own institution's submissions
        if current_user.institution_id != submission.institution_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        # External users can only update to certain statuses
        if status not in ["draft", "submitted"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="External users can only update status to 'draft' or 'submitted'"
            )
    
    # Update submission status
    submission.status = status
    db.commit()
    db.refresh(submission)
    
    return submission

async def process_submission_file(submission_id: int, file_path: str, file_ext: str, db: Session) -> None:
    """
    Process submission file and extract data.
    """
    data_points = []
    
    # Process file based on extension
    if file_ext == '.csv':
        # Process CSV file
        df = pd.read_csv(file_path)
        
        # Assuming CSV has columns: mdrm_identifier, value
        for _, row in df.iterrows():
            mdrm_identifier = row.get('mdrm_identifier')
            value = row.get('value')
            
            if mdrm_identifier and value is not None:
                data_points.append({
                    'mdrm_identifier': mdrm_identifier,
                    'value': str(value)
                })
    
    elif file_ext in ['.xlsx', '.xls']:
        # Process Excel file
        df = pd.read_excel(file_path)
        
        # Assuming Excel has columns: mdrm_identifier, value
        for _, row in df.iterrows():
            mdrm_identifier = row.get('mdrm_identifier')
            value = row.get('value')
            
            if mdrm_identifier and value is not None:
                data_points.append({
                    'mdrm_identifier': mdrm_identifier,
                    'value': str(value)
                })
    
    elif file_ext == '.xml':
        # Process XML file
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Assuming XML structure: <data><item mdrm="MDRM1">value1</item>...</data>
        for item in root.findall('.//item'):
            mdrm_identifier = item.get('mdrm')
            value = item.text
            
            if mdrm_identifier and value:
                data_points.append({
                    'mdrm_identifier': mdrm_identifier,
                    'value': value
                })
    
    elif file_ext == '.json':
        # Process JSON file
        with open(file_path, 'r') as f:
            json_data = json.load(f)
        
        # Assuming JSON structure: [{"mdrm_identifier": "MDRM1", "value": "value1"}, ...]
        for item in json_data:
            mdrm_identifier = item.get('mdrm_identifier')
            value = item.get('value')
            
            if mdrm_identifier and value is not None:
                data_points.append({
                    'mdrm_identifier': mdrm_identifier,
                    'value': str(value)
                })
    
    # Save data points to database
    for data_point in data_points:
        submitted_data = SubmittedData(
            submission_id=submission_id,
            mdrm_identifier=data_point['mdrm_identifier'],
            reported_value=data_point['value']
        )
        
        db.add(submitted_data)
    
    db.commit()


















