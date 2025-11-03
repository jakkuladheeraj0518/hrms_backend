from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services import separation_service
from app.schemas.separation_schema import PendingExitItem
from app.database.session import get_db

router = APIRouter()

@router.get("/pending-exits", response_model=list[PendingExitItem])
def pending_exits(db: Session = Depends(get_db)):
    return separation_service.fetch_pending_exits(db)
