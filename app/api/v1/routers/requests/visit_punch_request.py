from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.services.request_service import VisitPunchRequestService
from app.schemas.request_schema import (
    VisitPunchRequest, VisitPunchRequestCreate, StatusUpdate, DeleteResponse
)

router = APIRouter(
    prefix="/visit-punch-requests",
    tags=["Visit Punch Requests"]
)

visit_punch_service = VisitPunchRequestService()

@router.post("/", response_model=VisitPunchRequest)
def create_visit_punch_request(request: VisitPunchRequestCreate, db: Session = Depends(get_db)):
    return visit_punch_service.create_visit_punch_request(db, request)

@router.get("/", response_model=List[VisitPunchRequest])
def get_visit_punch_requests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return visit_punch_service.get_all(db, skip, limit)

@router.get("/{request_id}", response_model=VisitPunchRequest)
def get_visit_punch_request(request_id: int, db: Session = Depends(get_db)):
    return visit_punch_service.get(db, request_id)

@router.patch("/{request_id}/status", response_model=VisitPunchRequest)
def update_request_status(request_id: int, status_update: StatusUpdate, db: Session = Depends(get_db)):
    return visit_punch_service.update_status(db, request_id, status_update.status)

@router.delete("/{request_id}", response_model=DeleteResponse)
def delete_visit_punch_request(request_id: int, db: Session = Depends(get_db)):
    return visit_punch_service.delete(db, request_id)



