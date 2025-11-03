# app/api/v1/routes/other_reports.py
from fastapi import APIRouter
from typing import List
from app.schemas import report_schema as rs

router = APIRouter(prefix="/reports/other", tags=["Other Reports"])


@router.get("/activity_logs", response_model=List[rs.ActivityLogResponse])
def list_activity_logs():
    return [{"id": 1, "user_name": "admin", "action": "login", "description": "User logged in"}]
