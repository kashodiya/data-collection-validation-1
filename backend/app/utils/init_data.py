




import os
import sys
from datetime import datetime, date
from pathlib import Path

# Add parent directory to path to allow importing from app
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.core.database import SessionLocal, init_db
from app.core.security import get_password_hash
from app.models.institution import Institution
from app.models.report_series import ReportSeries
from app.models.mdrm import MDRMItem
from app.models.user import User
from app.models.validation_rule import ValidationRule

def init_sample_data():
    """Initialize database with sample data."""
    # Initialize database
    init_db()
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(User).first():
            print("Sample data already exists. Skipping initialization.")
            return
        
        print("Initializing sample data...")
        
        # Create institutions
        institutions = [
            Institution(
                rssd_id="1234567",
                name="First National Bank",
                institution_type="Commercial Bank",
                contact_info="123 Main St, Anytown, USA",
                status="active"
            ),
            Institution(
                rssd_id="7654321",
                name="Second State Bank",
                institution_type="State Bank",
                contact_info="456 Oak Ave, Somewhere, USA",
                status="active"
            ),
            Institution(
                rssd_id="9876543",
                name="Third Credit Union",
                institution_type="Credit Union",
                contact_info="789 Pine Rd, Nowhere, USA",
                status="active"
            )
        ]
        
        db.add_all(institutions)
        db.commit()
        
        # Create report series
        report_series = [
            ReportSeries(
                series_code="FR Y-9C",
                series_name="Consolidated Financial Statements for Holding Companies",
                description="Quarterly financial data for bank holding companies",
                filing_frequency="quarterly",
                status="active"
            ),
            ReportSeries(
                series_code="FFIEC 031",
                series_name="Consolidated Reports of Condition and Income for Banks",
                description="Quarterly financial data for banks with domestic and foreign offices",
                filing_frequency="quarterly",
                status="active"
            ),
            ReportSeries(
                series_code="FR 2052a",
                series_name="Complex Institution Liquidity Monitoring Report",
                description="Detailed reporting of liquidity risks",
                filing_frequency="monthly",
                status="active"
            )
        ]
        
        db.add_all(report_series)
        db.commit()
        
        # Create MDRM items
        mdrm_items = [
            MDRMItem(
                mdrm_identifier="BHCK2170",
                item_name="Total Assets",
                item_definition="The sum of all assets owned by the institution",
                data_type="numeric",
                valid_values="Positive number",
                series_mnemonic="FR Y-9C",
                effective_date=date(2020, 1, 1)
            ),
            MDRMItem(
                mdrm_identifier="BHCK2948",
                item_name="Total Liabilities",
                item_definition="The sum of all liabilities owed by the institution",
                data_type="numeric",
                valid_values="Positive number",
                series_mnemonic="FR Y-9C",
                effective_date=date(2020, 1, 1)
            ),
            MDRMItem(
                mdrm_identifier="BHCK3210",
                item_name="Total Equity Capital",
                item_definition="The total equity capital of the institution",
                data_type="numeric",
                valid_values="Positive number",
                series_mnemonic="FR Y-9C",
                effective_date=date(2020, 1, 1)
            ),
            MDRMItem(
                mdrm_identifier="RCON2170",
                item_name="Total Assets",
                item_definition="The sum of all assets owned by the institution",
                data_type="numeric",
                valid_values="Positive number",
                series_mnemonic="FFIEC 031",
                effective_date=date(2020, 1, 1)
            ),
            MDRMItem(
                mdrm_identifier="RCON2948",
                item_name="Total Liabilities",
                item_definition="The sum of all liabilities owed by the institution",
                data_type="numeric",
                valid_values="Positive number",
                series_mnemonic="FFIEC 031",
                effective_date=date(2020, 1, 1)
            )
        ]
        
        db.add_all(mdrm_items)
        db.commit()
        
        # Create validation rules
        validation_rules = [
            ValidationRule(
                rule_name="Assets Equal Liabilities Plus Equity",
                rule_description="Total Assets must equal Total Liabilities plus Total Equity Capital",
                rule_type="mathematical",
                rule_definition="BHCK2170 = BHCK2948 + BHCK3210",
                severity="error",
                effective_date=date(2020, 1, 1)
            ),
            ValidationRule(
                rule_name="Assets Must Be Positive",
                rule_description="Total Assets must be greater than zero",
                rule_type="range",
                rule_definition="BHCK2170 > 0",
                severity="error",
                effective_date=date(2020, 1, 1)
            ),
            ValidationRule(
                rule_name="Liabilities Must Be Positive",
                rule_description="Total Liabilities must be greater than zero",
                rule_type="range",
                rule_definition="BHCK2948 > 0",
                severity="error",
                effective_date=date(2020, 1, 1)
            )
        ]
        
        db.add_all(validation_rules)
        db.commit()
        
        # Create users
        users = [
            User(
                username="admin",
                password_hash=get_password_hash("admin123"),
                email="admin@example.com",
                role="admin",
                status="active"
            ),
            User(
                username="analyst",
                password_hash=get_password_hash("analyst123"),
                email="analyst@example.com",
                role="analyst",
                status="active"
            ),
            User(
                username="bank1",
                password_hash=get_password_hash("bank123"),
                email="bank1@example.com",
                role="external",
                institution_id=1,
                status="active"
            ),
            User(
                username="bank2",
                password_hash=get_password_hash("bank123"),
                email="bank2@example.com",
                role="external",
                institution_id=2,
                status="active"
            )
        ]
        
        db.add_all(users)
        db.commit()
        
        print("Sample data initialized successfully.")
        
    except Exception as e:
        print(f"Error initializing sample data: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_sample_data()




