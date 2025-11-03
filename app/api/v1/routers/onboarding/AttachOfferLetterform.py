from fastapi import APIRouter, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models
from app.database.session import get_db
from app.schemas.onboarding import (
	OfferLetterCreate,
	OfferLetterFormUpdate,
	OnboardingCandidateResponse,
	OfferLetterResponse,
	OfferLetterUpdate,
)
from app.models.onboarding import OfferLetter
router = APIRouter(
	prefix="/onboarding/offerletter",
	tags=["Offer Letter Form"]
)

# Dependency (imported above)


# ================================
# Create Offer Letter Entry
# ================================
@router.post("/attach", response_model=OfferLetterResponse)
def attach_offer_letter(data: OfferLetterCreate, db: Session = Depends(get_db)):
	# Ensure the candidate exists before creating the OfferLetter to avoid
	# a database-level foreign key violation which results in a 500 error.
	candidate = db.query(models.Candidate).filter(models.Candidate.id == data.candidate_id).first()
	if not candidate:
		raise HTTPException(status_code=404, detail="Candidate not found; cannot attach offer letter")

	try:
		new_offer = models.OfferLetter(
			candidate_id=data.candidate_id,
			offer_template=data.offer_template,
			gross_salary=data.gross_salary,
			salary_breakup=data.salary_breakup,
			esi_options=data.esi_options,
			pf_options=data.pf_options,
			professional_tax=data.professional_tax,
			income_tax=data.income_tax,
			lwf=data.lwf,
			employee_profile=data.employee_profile,
			joining_date=data.joining_date,
			confirmation_date=data.confirmation_date,
			dob=data.dob,
			notice_period=data.notice_period,
			gender=data.gender
		)
		db.add(new_offer)
		db.commit()
		db.refresh(new_offer)
		return new_offer
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


# ================================
# Get Offer Letter by Candidate
# ================================
@router.get("/candidate/{candidate_id}", response_model=OfferLetterResponse)
def get_offer_letter(candidate_id: int, db: Session = Depends(get_db)):
	offer = db.query(models.OfferLetter).filter(models.OfferLetter.candidate_id == candidate_id).first()
	if not offer:
		raise HTTPException(status_code=404, detail="Offer letter not found for this candidate")
	return offer


# ================================
# Update Offer Letter Details
# ================================
@router.put("/update/{offer_id}", response_model=OfferLetterResponse)
def update_offer_letter(offer_id: int, data: OfferLetterUpdate, db: Session = Depends(get_db)):
	offer = db.query(models.OfferLetter).filter(models.OfferLetter.id == offer_id).first()
	if not offer:
		raise HTTPException(status_code=404, detail="Offer letter not found")

	for key, value in data.dict(exclude_unset=True).items():
		setattr(offer, key, value)

	db.commit()
	db.refresh(offer)
	return offer


# ================================
# Delete Offer Letter
# ================================
@router.delete("/delete/{offer_id}")
def delete_offer_letter(offer_id: int, db: Session = Depends(get_db)):
	offer = db.query(models.OfferLetter).filter(models.OfferLetter.id == offer_id).first()
	if not offer:
		raise HTTPException(status_code=404, detail="Offer letter not found")
	db.delete(offer)
	db.commit()
	return {"message": "Offer letter deleted successfully"}
