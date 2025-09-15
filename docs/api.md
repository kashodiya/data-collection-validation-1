





























































# Federal Reserve Data Collection System API Documentation

## Authentication

### Login

```
POST /api/v1/auth/login
```

Authenticates a user and returns an access token.

**Request Body:**
- `username` (string, required): User's username
- `password` (string, required): User's password

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Logout

```
POST /api/v1/auth/logout
```

Logs out the current user.

**Headers:**
- `Authorization` (string, required): Bearer token

**Response:**
```json
{
  "detail": "Successfully logged out"
}
```

### Get User Profile

```
GET /api/v1/auth/profile
```

Returns the current user's profile.

**Headers:**
- `Authorization` (string, required): Bearer token

**Response:**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "role": "admin",
  "institution_id": null,
  "status": "active",
  "last_login": "2025-09-15T12:00:00"
}
```

## Institutions

### List Institutions

```
GET /api/v1/institutions/
```

Returns a list of institutions.

**Headers:**
- `Authorization` (string, required): Bearer token

**Query Parameters:**
- `skip` (integer, optional): Number of records to skip (default: 0)
- `limit` (integer, optional): Maximum number of records to return (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "rssd_id": "1234567",
    "name": "First National Bank",
    "institution_type": "Commercial Bank",
    "contact_info": "123 Main St, Anytown, USA",
    "status": "active",
    "created_at": "2025-09-15T12:00:00",
    "updated_at": "2025-09-15T12:00:00"
  }
]
```

### Create Institution

```
POST /api/v1/institutions/
```

Creates a new institution.

**Headers:**
- `Authorization` (string, required): Bearer token

**Request Body:**
```json
{
  "rssd_id": "1234567",
  "name": "First National Bank",
  "institution_type": "Commercial Bank",
  "contact_info": "123 Main St, Anytown, USA",
  "status": "active"
}
```

**Response:**
```json
{
  "id": 1,
  "rssd_id": "1234567",
  "name": "First National Bank",
  "institution_type": "Commercial Bank",
  "contact_info": "123 Main St, Anytown, USA",
  "status": "active",
  "created_at": "2025-09-15T12:00:00",
  "updated_at": "2025-09-15T12:00:00"
}
```

### Get Institution

```
GET /api/v1/institutions/{institution_id}
```

Returns a specific institution.

**Headers:**
- `Authorization` (string, required): Bearer token

**Path Parameters:**
- `institution_id` (integer, required): Institution ID

**Response:**
```json
{
  "id": 1,
  "rssd_id": "1234567",
  "name": "First National Bank",
  "institution_type": "Commercial Bank",
  "contact_info": "123 Main St, Anytown, USA",
  "status": "active",
  "created_at": "2025-09-15T12:00:00",
  "updated_at": "2025-09-15T12:00:00"
}
```

### Update Institution

```
PUT /api/v1/institutions/{institution_id}
```

Updates a specific institution.

**Headers:**
- `Authorization` (string, required): Bearer token

**Path Parameters:**
- `institution_id` (integer, required): Institution ID

**Request Body:**
```json
{
  "name": "Updated Bank Name",
  "contact_info": "456 New St, Newtown, USA",
  "status": "inactive"
}
```

**Response:**
```json
{
  "id": 1,
  "rssd_id": "1234567",
  "name": "Updated Bank Name",
  "institution_type": "Commercial Bank",
  "contact_info": "456 New St, Newtown, USA",
  "status": "inactive",
  "created_at": "2025-09-15T12:00:00",
  "updated_at": "2025-09-15T12:30:00"
}
```

### Delete Institution

```
DELETE /api/v1/institutions/{institution_id}
```

Deletes a specific institution.

**Headers:**
- `Authorization` (string, required): Bearer token

**Path Parameters:**
- `institution_id` (integer, required): Institution ID

**Response:**
- Status code 204 (No Content)

## MDRM Items

### List MDRM Items

```
GET /api/v1/mdrm/items
```

Returns a list of MDRM items.

**Headers:**
- `Authorization` (string, required): Bearer token

**Query Parameters:**
- `skip` (integer, optional): Number of records to skip (default: 0)
- `limit` (integer, optional): Maximum number of records to return (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "mdrm_identifier": "BHCK2170",
    "item_name": "Total Assets",
    "item_definition": "The sum of all assets owned by the institution",
    "data_type": "numeric",
    "valid_values": "Positive number",
    "series_mnemonic": "FR Y-9C",
    "effective_date": "2020-01-01",
    "end_date": null,
    "created_at": "2025-09-15T12:00:00",
    "updated_at": "2025-09-15T12:00:00"
  }
]
```

### Import MDRM Dictionary

```
POST /api/v1/mdrm/import
```

Imports MDRM dictionary from a CSV file.

**Headers:**
- `Authorization` (string, required): Bearer token

**Request Body:**
- `file` (file, required): CSV file containing MDRM dictionary

**Response:**
```json
{
  "detail": "Successfully imported 100 new MDRM items and updated 50 existing items"
}
```

### Search MDRM Items

```
GET /api/v1/mdrm/search
```

Searches for MDRM items.

**Headers:**
- `Authorization` (string, required): Bearer token

**Query Parameters:**
- `query` (string, required): Search query
- `series_mnemonic` (string, optional): Filter by series mnemonic

**Response:**
```json
[
  {
    "id": 1,
    "mdrm_identifier": "BHCK2170",
    "item_name": "Total Assets",
    "item_definition": "The sum of all assets owned by the institution",
    "data_type": "numeric",
    "valid_values": "Positive number",
    "series_mnemonic": "FR Y-9C",
    "effective_date": "2020-01-01",
    "end_date": null,
    "created_at": "2025-09-15T12:00:00",
    "updated_at": "2025-09-15T12:00:00"
  }
]
```

### Get MDRM Items for Series

```
GET /api/v1/mdrm/series/{series_id}
```

Returns MDRM items for a specific report series.

**Headers:**
- `Authorization` (string, required): Bearer token

**Path Parameters:**
- `series_id` (string, required): Series mnemonic

**Response:**
```json
[
  {
    "id": 1,
    "mdrm_identifier": "BHCK2170",
    "item_name": "Total Assets",
    "item_definition": "The sum of all assets owned by the institution",
    "data_type": "numeric",
    "valid_values": "Positive number",
    "series_mnemonic": "FR Y-9C",
    "effective_date": "2020-01-01",
    "end_date": null,
    "created_at": "2025-09-15T12:00:00",
    "updated_at": "2025-09-15T12:00:00"
  }
]
```

## Report Series

### List Report Series

```
GET /api/v1/report-series/
```

Returns a list of report series.

**Headers:**
- `Authorization` (string, required): Bearer token

**Query Parameters:**
- `skip` (integer, optional): Number of records to skip (default: 0)
- `limit` (integer, optional): Maximum number of records to return (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "series_code": "FR Y-9C",
    "series_name": "Consolidated Financial Statements for Holding Companies",
    "description": "Quarterly financial data for bank holding companies",
    "filing_frequency": "quarterly",
    "form_pdf_path": "/uploads/forms/FR_Y-9C_form.pdf",
    "instructions_pdf_path": "/uploads/forms/FR_Y-9C_instructions.pdf",
    "status": "active",
    "created_at": "2025-09-15T12:00:00",
    "updated_at": "2025-09-15T12:00:00"
  }
]
```

### Create Report Series

```
POST /api/v1/report-series/
```

Creates a new report series.

**Headers:**
- `Authorization` (string, required): Bearer token

**Request Body:**
```json
{
  "series_code": "FR Y-9C",
  "series_name": "Consolidated Financial Statements for Holding Companies",
  "description": "Quarterly financial data for bank holding companies",
  "filing_frequency": "quarterly",
  "form_pdf_path": null,
  "instructions_pdf_path": null,
  "status": "active"
}
```

**Response:**
```json
{
  "id": 1,
  "series_code": "FR Y-9C",
  "series_name": "Consolidated Financial Statements for Holding Companies",
  "description": "Quarterly financial data for bank holding companies",
  "filing_frequency": "quarterly",
  "form_pdf_path": null,
  "instructions_pdf_path": null,
  "status": "active",
  "created_at": "2025-09-15T12:00:00",
  "updated_at": "2025-09-15T12:00:00"
}
```

### Get Report Series

```
GET /api/v1/report-series/{report_series_id}
```

Returns a specific report series.

**Headers:**
- `Authorization` (string, required): Bearer token

**Path Parameters:**
- `report_series_id` (integer, required): Report series ID

**Response:**
```json
{
  "id": 1,
  "series_code": "FR Y-9C",
  "series_name": "Consolidated Financial Statements for Holding Companies",
  "description": "Quarterly financial data for bank holding companies",
  "filing_frequency": "quarterly",
  "form_pdf_path": "/uploads/forms/FR_Y-9C_form.pdf",
  "instructions_pdf_path": "/uploads/forms/FR_Y-9C_instructions.pdf",
  "status": "active",
  "created_at": "2025-09-15T12:00:00",
  "updated_at": "2025-09-15T12:00:00"
}
```

### Update Report Series

```
PUT /api/v1/report-series/{report_series_id}
```

Updates a specific report series.

**Headers:**
- `Authorization` (string, required): Bearer token

**Path Parameters:**
- `report_series_id` (integer, required): Report series ID

**Request Body:**
```json
{
  "description": "Updated description",
  "status": "inactive"
}
```

**Response:**
```json
{
  "id": 1,
  "series_code": "FR Y-9C",
  "series_name": "Consolidated Financial Statements for Holding Companies",
  "description": "Updated description",
  "filing_frequency": "quarterly",
  "form_pdf_path": "/uploads/forms/FR_Y-9C_form.pdf",
  "instructions_pdf_path": "/uploads/forms/FR_Y-9C_instructions.pdf",
  "status": "inactive",
  "created_at": "2025-09-15T12:00:00",
  "updated_at": "2025-09-15T12:30:00"
}
```

### Delete Report Series

```
DELETE /api/v1/report-series/{report_series_id}
```

Deletes a specific report series.

**Headers:**
- `Authorization` (string, required): Bearer token

**Path Parameters:**
- `report_series_id` (integer, required): Report series ID

**Response:**
- Status code 204 (No Content)





























































