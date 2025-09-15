












from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session
import pandas as pd
from datetime import datetime

from ....core.database import get_db
from ....core.security import get_current_active_user, check_permissions
from ....models.mdrm import MDRMItem
from ....models.user import User
from ....schemas.mdrm import MDRMItemCreate, MDRMItemUpdate, MDRMItemResponse

router = APIRouter()

@router.get("/items", response_model=List[MDRMItemResponse])
def get_mdrm_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Retrieve MDRM items.
    """
    mdrm_items = db.query(MDRMItem).offset(skip).limit(limit).all()
    return mdrm_items

@router.post("/import", status_code=status.HTTP_201_CREATED)
async def import_mdrm_dictionary(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Import MDRM dictionary from CSV file.
    
    - Only analysts and admins can import MDRM dictionary
    """
    # Check permissions
    if not check_permissions("analyst", current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Check file extension
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV files are supported"
        )
    
    try:
        # Read CSV file
        contents = await file.read()
        df = pd.read_csv(pd.io.common.BytesIO(contents))
        
        # Process and import data
        imported_count = 0
        updated_count = 0
        
        for _, row in df.iterrows():
            # Check if MDRM item already exists
            mdrm_identifier = row.get('mdrm_identifier')
            if not mdrm_identifier:
                continue
                
            db_mdrm_item = db.query(MDRMItem).filter(
                MDRMItem.mdrm_identifier == mdrm_identifier
            ).first()
            
            # Parse effective date
            effective_date_str = row.get('effective_date')
            try:
                effective_date = datetime.strptime(effective_date_str, '%Y-%m-%d').date()
            except (ValueError, TypeError):
                effective_date = datetime.now().date()
            
            # Parse end date if available
            end_date = None
            end_date_str = row.get('end_date')
            if end_date_str:
                try:
                    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                except (ValueError, TypeError):
                    pass
            
            if db_mdrm_item:
                # Update existing item
                db_mdrm_item.item_name = row.get('item_name', db_mdrm_item.item_name)
                db_mdrm_item.item_definition = row.get('item_definition', db_mdrm_item.item_definition)
                db_mdrm_item.data_type = row.get('data_type', db_mdrm_item.data_type)
                db_mdrm_item.valid_values = row.get('valid_values', db_mdrm_item.valid_values)
                db_mdrm_item.series_mnemonic = row.get('series_mnemonic', db_mdrm_item.series_mnemonic)
                db_mdrm_item.effective_date = effective_date
                if end_date:
                    db_mdrm_item.end_date = end_date
                
                updated_count += 1
            else:
                # Create new item
                mdrm_item = MDRMItem(
                    mdrm_identifier=mdrm_identifier,
                    item_name=row.get('item_name', ''),
                    item_definition=row.get('item_definition'),
                    data_type=row.get('data_type', 'string'),
                    valid_values=row.get('valid_values'),
                    series_mnemonic=row.get('series_mnemonic'),
                    effective_date=effective_date,
                    end_date=end_date
                )
                
                db.add(mdrm_item)
                imported_count += 1
        
        db.commit()
        
        return {
            "detail": f"Successfully imported {imported_count} new MDRM items and updated {updated_count} existing items"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error importing MDRM dictionary: {str(e)}"
        )

@router.get("/search", response_model=List[MDRMItemResponse])
def search_mdrm_items(
    query: str = Query(..., description="Search query"),
    series_mnemonic: Optional[str] = Query(None, description="Filter by series mnemonic"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Search MDRM items by query string.
    """
    # Build query
    db_query = db.query(MDRMItem)
    
    # Apply filters
    db_query = db_query.filter(
        (MDRMItem.mdrm_identifier.ilike(f"%{query}%")) |
        (MDRMItem.item_name.ilike(f"%{query}%")) |
        (MDRMItem.item_definition.ilike(f"%{query}%"))
    )
    
    if series_mnemonic:
        db_query = db_query.filter(MDRMItem.series_mnemonic == series_mnemonic)
    
    # Execute query
    mdrm_items = db_query.limit(100).all()
    
    return mdrm_items

@router.get("/series/{series_id}", response_model=List[MDRMItemResponse])
def get_mdrm_items_for_series(
    series_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get MDRM items for a specific report series.
    """
    mdrm_items = db.query(MDRMItem).filter(
        MDRMItem.series_mnemonic == series_id
    ).all()
    
    return mdrm_items












