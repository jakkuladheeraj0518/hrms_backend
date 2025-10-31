from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.services.request_service import WorkflowRequestService
from app.schemas.request_schema import (
    WorkflowRequest, WorkflowRequestCreate, StatusUpdate, DeleteResponse
)

router = APIRouter(
    prefix="/workflow-requests",
    tags=["Workflow Requests"]
)

workflow_service = WorkflowRequestService()

@router.post("/", response_model=WorkflowRequest)
def create_workflow_request(request: WorkflowRequestCreate, db: Session = Depends(get_db)):
    return workflow_service.create_workflow_request(db, request)

@router.get("/", response_model=List[WorkflowRequest])
def get_workflow_requests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return workflow_service.get_all(db, skip, limit)

@router.get("/{request_id}", response_model=WorkflowRequest)
def get_workflow_request(request_id: int, db: Session = Depends(get_db)):
    return workflow_service.get(db, request_id)

@router.patch("/{request_id}/status", response_model=WorkflowRequest)
def update_request_status(request_id: int, status_update: StatusUpdate, db: Session = Depends(get_db)):
    return workflow_service.update_status(db, request_id, status_update.status)

@router.delete("/{request_id}", response_model=DeleteResponse)
def delete_workflow_request(request_id: int, db: Session = Depends(get_db)):
    return workflow_service.delete(db, request_id)



