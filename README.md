























# Federal Reserve Data Collection System

A web-based data collection system for financial institutions to submit regulatory reports to the Federal Reserve. The system manages MDRM (Micro Data Reference Manual) data elements, validates submissions using configurable rules, and supports multiple report series with flexible data formats.

## Project Development

This project was completely developed using OpenHands AI based on the detailed requirements document. The AI assistant was used to generate the entire codebase, including backend, frontend, and documentation.

The detailed requirements document can be found in the [docs/requirements.md](docs/requirements.md) file.

## Project Structure

```
project/
├── backend/               # FastAPI backend
│   ├── app/
│   │   ├── api/           # API endpoints
│   │   ├── core/          # Core functionality
│   │   ├── models/        # Database models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   └── utils/         # Utility functions
│   ├── requirements.txt   # Python dependencies
│   └── run.py             # Application entry point
├── frontend/              # React frontend
│   ├── public/            # Static files
│   ├── src/               # Source code
│   │   ├── components/    # Reusable components
│   │   ├── context/       # React context
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   └── utils/         # Utility functions
│   └── package.json       # Node.js dependencies
└── README.md              # Project documentation
```

## Features

- **Data Management**: Manage MDRM data elements as defined in the Federal Reserve's Micro Data Reference Manual
- **Institution Management**: Register and manage financial institutions
- **Data Submission**: Web-based data upload supporting multiple formats (CSV, Excel, XML, JSON)
- **Validation Engine**: Flexible system for defining and executing validation rules
- **Report Generation**: Generate reports showing submitted data and validation results
- **Form and Instruction Management**: Store and manage PDF report forms and instructions

## Technology Stack

- **Backend**: Python with FastAPI
- **Database**: SQLite
- **Frontend**: React
- **Authentication**: JWT-based authentication

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd project/backend
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python run.py
   ```

The backend API will be available at http://localhost:51209.

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd project/frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Run the development server:
   ```
   npm start
   ```

The frontend application will be available at http://localhost:3000.

## API Documentation

API documentation is available at http://localhost:51209/docs when the backend is running.

## User Roles

- **External Users**: Financial institution representatives who can submit reports
- **Internal Analysts**: Federal Reserve staff who can review and validate submissions
- **Admin Users**: System administrators with full access to all features

## Demo Credentials

- **Admin**: admin / admin123
- **Analyst**: analyst / analyst123
- **Bank**: bank1 / bank123























