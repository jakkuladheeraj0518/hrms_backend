from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.services.request_service import CompOffRequestService
from app.schemas.request_schema import (
    CompOffRequest, CompOffRequestCreate, StatusUpdate, DeleteResponse
)

router = APIRouter(
    prefix="/compoff-requests",
    tags=["Comp Off Requests"]
)

# Initialize service
compoff_service = CompOffRequestService()

@router.post("/", response_model=CompOffRequest)
def create_compoff_request(
    request: CompOffRequestCreate,
    db: Session = Depends(get_db)
):
    """Create a new comp off request"""
    return compoff_service.create_compoff_request(db, request)

@router.get("/", response_model=List[CompOffRequest])
def get_compoff_requests(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all comp off requests"""
    return compoff_service.get_all(db, skip, limit)

@router.get("/{request_id}", response_model=CompOffRequest)
def get_compoff_request(request_id: int, db: Session = Depends(get_db)):
    """Get a specific comp off request by ID"""
    return compoff_service.get(db, request_id)

@router.patch("/{request_id}/status", response_model=CompOffRequest)
def update_request_status(
    request_id: int,
    status_update: StatusUpdate,
    db: Session = Depends(get_db)
):
    """Update the status of a comp off request"""
    return compoff_service.update_status(db, request_id, status_update.status)

@router.delete("/{request_id}", response_model=DeleteResponse)
def delete_compoff_request(request_id: int, db: Session = Depends(get_db)):
    """Delete a comp off request"""
    return compoff_service.delete(db, request_id)



