from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.database.session import get_db
from app.services.request_service import LeaveRequestService
from app.schemas.request_schema import (
    LeaveRequest, LeaveRequestCreate, StatusUpdate, DeleteResponse
)

router = APIRouter(
    prefix="/leave-requests",
    tags=["Leave Requests"]
)

# Initialize service
leave_service = LeaveRequestService()

@router.post("/", response_model=LeaveRequest)
def create_leave_request(
    request: LeaveRequestCreate,
    db: Session = Depends(get_db)
):
    """Create a new leave request"""
    return leave_service.create_leave_request(db, request)

@router.get("/", response_model=List[LeaveRequest])
def get_leave_requests(
    skip: int = 0,
    limit: int = 100,
    location: Optional[str] = None,
    status: Optional[str] = None,
    leave_type: Optional[str] = None,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all leave requests with filters"""
    return leave_service.get_filtered_requests(
        db, skip, limit, location, status, leave_type, from_date, to_date, search
    )

@router.get("/{request_id}", response_model=LeaveRequest)
def get_leave_request(request_id: int, db: Session = Depends(get_db)):
    """Get a specific leave request by ID"""
    return leave_service.get(db, request_id)

@router.patch("/{request_id}/status", response_model=LeaveRequest)
def update_request_status(
    request_id: int,
    status_update: StatusUpdate,
    db: Session = Depends(get_db)
):
    """Update the status of a leave request (Approve/Reject)"""
    return leave_service.update_status(db, request_id, status_update.status)

@router.delete("/{request_id}", response_model=DeleteResponse)
def delete_leave_request(request_id: int, db: Session = Depends(get_db)):
    """Delete a leave request"""
    return leave_service.delete(db, request_id)

@router.get("/stats/count")
def get_request_count(
    location: Optional[str] = None,
    status: Optional[str] = None,
    leave_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get count of leave requests"""
    return leave_service.get_request_count(db, location, status, leave_type)



