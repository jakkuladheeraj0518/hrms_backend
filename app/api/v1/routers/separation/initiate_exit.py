from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import separation_schema
from app.services import separation_service
from app.database.session import get_db

router = APIRouter()

# 🔹 Test Route
@router.get("/test")
def test_route():
    return {"message": "Initiate Exit API working successfully!"}


# 🔹 POST API — Add new separation record
@router.post("/initiate-exit", response_model=separation_schema.InitiatedExitResponse)
def initiate_exit(data: separation_schema.InitiatedExitCreate, db: Session = Depends(get_db)):
    return separation_service.initiate_exit(db, data)


# 🔹 GET API — Show all separation records
@router.get("/show", response_model=list[separation_schema.InitiatedExitResponse])
def show_all_exits(db: Session = Depends(get_db)):
    return separation_service.get_all_exits(db)
