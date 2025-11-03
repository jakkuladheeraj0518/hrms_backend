from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services import separation_service
from app.database.session import get_db

router = APIRouter()

@router.get("/dashboard")
def get_dashboard(db: Session = Depends(get_db)):
    return separation_service.dashboard_data(db)
