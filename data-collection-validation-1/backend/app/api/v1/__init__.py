

from fastapi import APIRouter

from .endpoints import auth, institutions, mdrm, report_series, submissions, validation, reports, forms

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(institutions.router, prefix="/institutions", tags=["Institutions"])
api_router.include_router(mdrm.router, prefix="/mdrm", tags=["MDRM"])
api_router.include_router(report_series.router, prefix="/report-series", tags=["Report Series"])
api_router.include_router(submissions.router, prefix="/submissions", tags=["Data Submissions"])
api_router.include_router(validation.router, prefix="/validation", tags=["Validation"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
api_router.include_router(forms.router, prefix="/forms", tags=["Forms"])

