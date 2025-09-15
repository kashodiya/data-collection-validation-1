# Federal Reserve Data Collection System - Requirements Document

## Project Overview

Create a web-based data collection system for financial institutions to submit regulatory reports to the Federal Reserve. The system manages MDRM (Micro Data Reference Manual) data elements, validates submissions using configurable rules, and supports multiple report series with flexible data formats.

## System Architecture

### Technology Stack
- **Backend**: Python with FastAPI (single server for web app and APIs)
- **Database**: SQLite 
- **Frontend**: React
- **Package Management**: uv (Python package manager)
- **Authentication**: Simple password-based system stored in database
- **Deployment**: Single server architecture

## Core Business Requirements

### 1. Data Management
- **MDRM Data Elements**: Manage data elements as defined in the Federal Reserve's Micro Data Reference Manual
- **Report Series**: Support multiple report series (e.g., FR Y-9C, FFIEC 031, etc.)
- **Data Dictionary Integration**: Import and manage MDRM data dictionary with metadata:
  - MDRM Identifier
  - Item Name  
  - Item Definition
  - Data Type
  - Valid Values/Ranges
  - Series Mnemonics
  - Effective Dates

### 2. Institution Management
- Register and manage financial institutions
- Institution profiles with:
  - Institution ID (RSSD ID)
  - Institution Name
  - Institution Type
  - Contact Information
  - Assigned Report Series
  - Filing Schedules

### 3. Data Submission System
- **Upload Interface**: Web-based data upload supporting multiple formats:
  - CSV files
  - Excel files (.xlsx, .xls)
  - XML format
  - JSON format
- **Bulk Upload**: Support batch submission of multiple reports
- **Data Mapping**: Map uploaded data to MDRM identifiers
- **Submission Tracking**: Track submission status and history

### 4. Validation Engine
- **Rule-Based Validation**: Flexible system for defining and executing validation rules
- **Rule Types**:
  - Data type validation (numeric, text, date)
  - Range validation (min/max values)
  - Format validation (patterns, lengths)
  - Cross-field validation (relationships between fields)
  - Historical validation (comparisons with previous submissions)
  - Mathematical validation (calculated fields, formulas)
- **Rule Management**: 
  - Create, modify, and deactivate rules
  - Rule versioning and effective dates
  - Rule priority and execution order
- **Error Handling**:
  - Detailed error messages with field references
  - Warning vs. critical error classification
  - Error correction workflow

### 5. Report Generation
- **Submission Reports**: Generate reports showing submitted data
- **Validation Reports**: Detailed validation results with errors/warnings
- **Historical Reports**: Trend analysis and historical comparisons
- **Export Formats**: PDF, Excel, CSV export options

### 6. Form and Instruction Management
- **PDF Form Storage**: Store and manage PDF report forms
- **Instructions**: Manage reporting instructions and guidance documents
- **Version Control**: Track form and instruction versions
- **Publication**: Make forms and instructions available to institutions

## Technical Requirements

### 1. Database Schema

#### Core Tables
```sql
-- Institutions
institutions (
    id, rssd_id, name, institution_type, 
    contact_info, status, created_at, updated_at
)

-- MDRM Data Dictionary
mdrm_items (
    id, mdrm_identifier, item_name, item_definition,
    data_type, valid_values, series_mnemonic, 
    effective_date, end_date, created_at, updated_at
)

-- Report Series
report_series (
    id, series_code, series_name, description,
    filing_frequency, form_pdf_path, instructions_pdf_path,
    status, created_at, updated_at
)

-- Data Submissions
data_submissions (
    id, institution_id, report_series_id, reporting_date,
    submission_date, file_path, status, 
    validation_status, created_at, updated_at
)

-- Submitted Data
submitted_data (
    id, submission_id, mdrm_identifier, 
    reported_value, calculated_value, 
    created_at, updated_at
)

-- Validation Rules
validation_rules (
    id, rule_name, rule_description, rule_type,
    rule_definition, severity, effective_date, 
    end_date, created_at, updated_at
)

-- Validation Results
validation_results (
    id, submission_id, rule_id, field_identifier,
    error_message, severity, status, 
    created_at, resolved_at
)

-- Users and Authentication
users (
    id, username, password_hash, email, 
    role, institution_id, status, 
    last_login, created_at, updated_at
)
```

### 2. API Endpoints

#### Authentication
- `POST /auth/login` - User authentication
- `POST /auth/logout` - User logout
- `GET /auth/profile` - Get user profile

#### Institution Management
- `GET /institutions` - List institutions
- `POST /institutions` - Create institution
- `GET /institutions/{id}` - Get institution details
- `PUT /institutions/{id}` - Update institution
- `DELETE /institutions/{id}` - Delete institution

#### MDRM Management
- `GET /mdrm/items` - List MDRM items
- `POST /mdrm/import` - Import MDRM dictionary
- `GET /mdrm/search` - Search MDRM items
- `GET /mdrm/series/{series_id}` - Get MDRM items for series

#### Data Submission
- `POST /submissions/upload` - Upload data file
- `GET /submissions` - List submissions
- `GET /submissions/{id}` - Get submission details
- `POST /submissions/{id}/validate` - Trigger validation
- `PUT /submissions/{id}/status` - Update submission status

#### Validation
- `GET /validation/rules` - List validation rules
- `POST /validation/rules` - Create validation rule
- `PUT /validation/rules/{id}` - Update validation rule
- `GET /validation/results/{submission_id}` - Get validation results

#### Reports
- `GET /reports/submissions/{id}` - Generate submission report
- `GET /reports/validation/{submission_id}` - Generate validation report
- `GET /reports/historical/{institution_id}` - Historical report

#### Forms and Instructions
- `GET /forms` - List available forms
- `GET /forms/{series_id}` - Get form for report series
- `GET /instructions/{series_id}` - Get instructions for report series

### 3. Frontend Components

#### Public Pages
- Login page
- Institution registration
- Form download page

#### Institution Dashboard
- Submission status overview
- Upcoming filing deadlines
- Historical submissions
- Download forms and instructions

#### Data Submission Flow
- File upload interface
- Data mapping and preview
- Validation results display
- Error correction workflow
- Submission confirmation

#### Internal Analyst Dashboard
- Institution management
- Validation rule management
- Submission monitoring
- Report generation
- Data quality analytics

#### Admin Dashboard
- User management
- System configuration
- MDRM dictionary management
- Form and instruction management
- System monitoring

### 4. File Processing
- **CSV Parser**: Handle various CSV formats and delimiters
- **Excel Parser**: Support .xlsx and .xls files
- **XML Parser**: Handle structured XML submissions
- **JSON Parser**: Process JSON formatted data
- **Data Validation**: Validate file structure before processing
- **Error Handling**: Graceful handling of malformed files

### 5. Validation Engine Architecture
```python
class ValidationEngine:
    def validate_submission(submission_id):
        # Load submission data
        # Load applicable validation rules
        # Execute rules in priority order
        # Store validation results
        # Generate validation report
        
class ValidationRule:
    def __init__(rule_definition):
        # Parse rule definition
        # Set up execution context
        
    def execute(data_row, historical_data):
        # Execute rule logic
        # Return validation result
```

### 6. Security Requirements
- Password hashing using bcrypt
- Session management
- Role-based access control (RBAC)
- File upload validation
- SQL injection prevention
- XSS protection
- CSRF protection
- Secure file storage

## User Roles and Permissions

### 1. External Users (Financial Institutions)
**Permissions:**
- View assigned report series
- Upload data submissions
- View submission history
- Download forms and instructions
- View validation results for own submissions
- Update institution profile

### 2. Internal Analysts
**Permissions:**
- All External User permissions
- View all institution submissions
- Create and modify validation rules
- Generate system reports
- Approve/reject submissions
- Manage MDRM data dictionary
- Access data analytics

### 3. Admin Users
**Permissions:**
- All Internal Analyst permissions
- User management (create, modify, delete users)
- Institution management
- System configuration
- Form and instruction management
- Database maintenance
- System monitoring and logs

## Data Formats and Standards

### 1. Upload Data Format
- **Primary**: CSV with predefined column structure
- **Alternative**: Excel with standard template
- **Advanced**: XML/JSON with schema validation

### 2. MDRM Integration
- Import MDRM data dictionary from Federal Reserve CSV format
- Support for MDRM identifier mapping
- Handle effective date ranges for data elements

### 3. File Naming Conventions
```
{InstitutionID}_{SeriesCode}_{ReportingDate}_{SubmissionDate}.{ext}
Example: 123456_FR2052A_20240331_20240415.csv
```

## Performance Requirements
- Support 1000+ concurrent users
- Handle files up to 100MB
- Validation processing within 5 minutes for standard submissions
- 99.9% uptime during business hours
- Database backup and recovery procedures

## Integration Requirements
- **MDRM Dictionary**: Automated import from Federal Reserve sources
- **Forms Repository**: Integration with Federal Reserve forms database
- **Email Notifications**: SMTP integration for submission notifications
- **File Storage**: Secure file storage with backup capabilities

## Monitoring and Logging
- Application logging (errors, warnings, info)
- User activity logging
- System performance monitoring
- Data submission tracking
- Validation rule execution logging
- Security event logging

## Development Guidelines

### 1. Project Structure
```
project/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── services/
│   │   └── utils/
│   ├── requirements.txt
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── utils/
│   └── package.json
├── database/
│   ├── migrations/
│   └── seeds/
├── docs/
└── tests/
```

### 2. Code Quality
- Use Python type hints
- Follow PEP 8 style guidelines
- Implement comprehensive error handling
- Write unit and integration tests
- Document all API endpoints
- Use meaningful variable and function names

### 3. Configuration Management
- Environment-based configuration
- Separate configs for development, testing, production
- Secure storage of sensitive configuration data

## Deployment Architecture
- Single server deployment
- SQLite database file storage
- Static file serving for forms and instructions
- Log rotation and management
- Automated backup procedures
- Health check endpoints

## Success Metrics
- System availability (target: 99.9%)
- Data validation accuracy (target: 99.5%)
- User satisfaction scores
- Submission processing time
- Error resolution time
- System performance metrics

## References
- You can learn about MDRM here: https://www.federalreserve.gov/data/mdrm.htm
- You can download MDRM data dictionary from: https://www.federalreserve.gov/apps/mdrm/pdf/MDRM.zip
- You can learn about data dictionary columns etc. here: https://www.federalreserve.gov/apps/mdrm/download_mdrm.htm
- FRB also publish a PDF form for each report. Along with the report we publish instructions. You can search such forms and instructions here: https://www.federalreserve.gov/apps/reportingforms
- You can find complete list of series or reports here: https://www.federalreserve.gov/apps/mdrm/series