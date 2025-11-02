from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.onboarding import OfferLetterForm
from app.schemas.onboarding import OfferLetterFormCreate, OfferLetterFormResponse




router = APIRouter(
    prefix="/offerletterform",
    tags=["OfferLetterForm"]
)

# Create Offer Letter Form
@router.post("/", response_model=OfferLetterFormResponse)
def create_offer_letter(form: OfferLetterFormCreate, db: Session = Depends(get_db)):
    db_form = OfferLetterForm(**form.dict())
    db.add(db_form)
    db.commit()
    db.refresh(db_form)
    return db_form

# Get All Offer Letters
@router.get("/", response_model=List[OfferLetterFormResponse])
def get_offer_letters(db: Session = Depends(get_db)):
    return db.query(OfferLetterForm).all()

# Get Offer Letter by ID
@router.get("/{form_id}", response_model=OfferLetterFormResponse)
def get_offer_letter(form_id: int, db: Session = Depends(get_db)):
    form = db.query(OfferLetterForm).filter(OfferLetterForm.id == form_id).first()
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")
    return form

# Update Offer Letter
@router.put("/{form_id}", response_model=OfferLetterFormResponse)
def update_offer_letter(form_id: int, form_data: OfferLetterFormCreate, db: Session = Depends(get_db)):
    form = db.query(OfferLetterForm).filter(OfferLetterForm.id == form_id).first()
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")
    for key, value in form_data.dict().items():
        setattr(form, key, value)
    db.commit()
    db.refresh(form)
    return form

# Delete Offer Letter
@router.delete("/{form_id}")
def delete_offer_letter(form_id: int, db: Session = Depends(get_db)):
    form = db.query(OfferLetterForm).filter(OfferLetterForm.id == form_id).first()
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")
    db.delete(form)
    db.commit()
    return {"detail": "Offer Letter deleted successfully"}
