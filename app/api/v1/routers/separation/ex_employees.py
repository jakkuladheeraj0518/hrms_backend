from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services import separation_service
from app.schemas.separation_schema import ExEmployeeItem
from app.database.session import get_db

router = APIRouter()

@router.get("/ex-employees", response_model=list[ExEmployeeItem])
def ex_employees(db: Session = Depends(get_db)):
    return separation_service.fetch_ex_employees(db)
