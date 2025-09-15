
































































# Federal Reserve Data Collection System - Setup Guide

This guide provides instructions for setting up the Federal Reserve Data Collection System for development and testing.

## Prerequisites

- Python 3.10 or higher
- Node.js 16 or higher
- npm 8 or higher

## Backend Setup

### 1. Create a Virtual Environment

```bash
cd project/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the `backend` directory with the following content:

```
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
UPLOAD_DIR=/path/to/upload/directory
```

### 4. Run the Application

```bash
python run.py
```

The backend API will be available at http://localhost:51209.

## Frontend Setup

### 1. Install Dependencies

```bash
cd project/frontend
npm install
```

### 2. Configure Environment Variables

Create a `.env` file in the `frontend` directory with the following content:

```
PORT=57699
REACT_APP_API_URL=http://localhost:51209/api/v1
```

### 3. Run the Application

```bash
npm start
```

The frontend application will be available at http://localhost:57699.

## Running Tests

### Backend Tests

```bash
cd project/backend
pytest
```

### Frontend Tests

```bash
cd project/frontend
npm test
```

## Database

The application uses SQLite as the database. The database file will be created automatically when the application is run for the first time.

## Sample Data

The application includes a script to initialize the database with sample data. This script is run automatically when the application starts.

### Sample Users

- **Admin**: admin / admin123
- **Analyst**: analyst / analyst123
- **Bank**: bank1 / bank123

## API Documentation

API documentation is available at http://localhost:51209/docs when the backend is running.

## Troubleshooting

### Backend Issues

- **Database errors**: Check that the database file is writable by the application.
- **Import errors**: Make sure all dependencies are installed.
- **Permission errors**: Check that the upload directory is writable by the application.

### Frontend Issues

- **API connection errors**: Make sure the backend is running and the API URL is correct.
- **Build errors**: Check that all dependencies are installed.
- **CORS errors**: Make sure the backend is configured to allow requests from the frontend.
































































