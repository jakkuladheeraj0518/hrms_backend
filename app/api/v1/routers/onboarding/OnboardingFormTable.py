from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.onboarding import OnboardingCandidate
from app.schemas.onboarding import OnboardingCandidateResponse
from typing import List

router = APIRouter(prefix="/onboardingfromtable", tags=["OnboardingFormTable"])

# List all candidates (with optional status filter)
@router.get("/candidates/", response_model=List[OnboardingCandidateResponse])
def list_candidates(status: str = None, db: Session = Depends(get_db)):
    query = db.query(OnboardingCandidate)
    if status:
        query = query.filter(OnboardingCandidate.form_status == status)
    return query.all()

# Approve a candidate form
@router.put("/candidate/{candidate_id}/approve", response_model=OnboardingCandidateResponse)
def approve_candidate(candidate_id: int, db: Session = Depends(get_db)):
    db_candidate = db.query(OnboardingCandidate).filter(OnboardingCandidate.id == candidate_id).first()
    if not db_candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    db_candidate.form_status = "Approved"
    db.commit()
    db.refresh(db_candidate)
    return db_candidate

# Reject a candidate form
@router.put("/candidate/{candidate_id}/reject", response_model=OnboardingCandidateResponse)
def reject_candidate(candidate_id: int, db: Session = Depends(get_db)):
    db_candidate = db.query(OnboardingCandidate).filter(OnboardingCandidate.id == candidate_id).first()
    if not db_candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    db_candidate.form_status = "Rejected"
    db.commit()
    db.refresh(db_candidate)
    return db_candidate
