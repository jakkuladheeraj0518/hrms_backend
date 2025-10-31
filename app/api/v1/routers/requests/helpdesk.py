from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.services.request_service import HelpdeskRequestService
from app.schemas.request_schema import (
    HelpdeskRequest, HelpdeskRequestCreate, StatusUpdate, DeleteResponse
)

router = APIRouter(
    prefix="/helpdesk-requests",
    tags=["Helpdesk Requests"]
)

# Initialize service
helpdesk_service = HelpdeskRequestService()

@router.post("/", response_model=HelpdeskRequest)
def create_helpdesk_request(
    request: HelpdeskRequestCreate,
    db: Session = Depends(get_db)
):
    """Create a new helpdesk request"""
    return helpdesk_service.create_helpdesk_request(db, request)

@router.get("/", response_model=List[HelpdeskRequest])
def get_helpdesk_requests(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all helpdesk requests"""
    return helpdesk_service.get_all(db, skip, limit)

@router.get("/{request_id}", response_model=HelpdeskRequest)
def get_helpdesk_request(request_id: int, db: Session = Depends(get_db)):
    """Get a specific helpdesk request by ID"""
    return helpdesk_service.get(db, request_id)

@router.patch("/{request_id}/status", response_model=HelpdeskRequest)
def update_request_status(
    request_id: int,
    status_update: StatusUpdate,
    db: Session = Depends(get_db)
):
    """Update the status of a helpdesk request"""
    return helpdesk_service.update_status(db, request_id, status_update.status)

@router.delete("/{request_id}", response_model=DeleteResponse)
def delete_helpdesk_request(request_id: int, db: Session = Depends(get_db)):
    """Delete a helpdesk request"""
    return helpdesk_service.delete(db, request_id)



