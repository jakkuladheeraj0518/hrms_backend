from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.onboarding import OnboardingCandidate
from app.schemas.onboarding import ReviewFormSchema
from app.database.session import get_db

router = APIRouter(prefix="/reviewform", tags=["ReviewForm"])

# Get candidate by ID
@router.get("/candidate/{candidate_id}", response_model=ReviewFormSchema)
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.query(OnboardingCandidate).filter(OnboardingCandidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate

# Approve form
@router.put("/candidate/{candidate_id}/approve", response_model=ReviewFormSchema)
def approve_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.query(OnboardingCandidate).filter(OnboardingCandidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    candidate.form_status = "Approved"
    db.commit()
    db.refresh(candidate)
    return candidate

# Reject form
@router.put("/candidate/{candidate_id}/reject", response_model=ReviewFormSchema)
def reject_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.query(OnboardingCandidate).filter(OnboardingCandidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    candidate.form_status = "Rejected"
    db.commit()
    db.refresh(candidate)
    return candidate

# Send back for corrections
@router.put("/candidate/{candidate_id}/sendback", response_model=ReviewFormSchema)
def send_back_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.query(OnboardingCandidate).filter(OnboardingCandidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    candidate.form_status = "Sent Back"
    db.commit()
    db.refresh(candidate)
    return candidate
