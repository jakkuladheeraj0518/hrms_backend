from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas import datacapture_schema as schemas
from app.services import datacapture_service as service
from app.models import datacapture as models
from app.database.session import get_db

router = APIRouter(prefix="/api/datacapture/it-declarations", tags=["IT Declarations"])

# =========================================================
# CREATE IT Declaration
# =========================================================
@router.post("/", response_model=schemas.ITDeclaration)
def create_it_declaration(declaration: schemas.ITDeclarationCreate, db: Session = Depends(get_db)):
    """Create a new IT Declaration record"""
    return service.create_it_declaration(db, declaration)


# =========================================================
# READ ALL IT Declarations
# =========================================================
@router.get("/", response_model=List[schemas.ITDeclaration])
def get_all_it_declarations(db: Session = Depends(get_db)):
    """Retrieve all IT Declaration records"""
    return service.get_it_declarations(db)


# =========================================================
# READ BY Employee Code + Financial Year
# =========================================================
@router.get("/{employee_code}/{financial_year}", response_model=schemas.ITDeclaration)
def get_it_declaration_by_employee(employee_code: str, financial_year: str, db: Session = Depends(get_db)):
    """Retrieve an IT Declaration for a specific employee and financial year"""
    declaration = service.get_it_declaration_by_employee(db, employee_code, financial_year)
    if not declaration:
        raise HTTPException(status_code=404, detail=f"No declaration found for employee {employee_code} in {financial_year}")
    return declaration


# =========================================================
# UPDATE IT Declaration
# =========================================================
@router.put("/{declaration_id}", response_model=schemas.ITDeclaration)
def update_it_declaration(declaration_id: int, declaration_update: schemas.ITDeclarationCreate, db: Session = Depends(get_db)):
    """Update an existing IT Declaration record"""
    updated = service.update_it_declaration(db, declaration_id, declaration_update)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Declaration with ID {declaration_id} not found")
    return updated


# =========================================================
# DELETE IT Declaration
# =========================================================
@router.delete("/{declaration_id}")
def delete_it_declaration(declaration_id: int, db: Session = Depends(get_db)):
    """Delete an IT Declaration record"""
    success = service.delete_it_declaration(db, declaration_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Declaration with ID {declaration_id} not found")
    return {"detail": f"IT Declaration record {declaration_id} deleted successfully"}
