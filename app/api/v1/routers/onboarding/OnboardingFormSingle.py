from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.onboarding import OnboardingCandidate
from app.schemas.onboarding import OnboardingCandidateCreate, OnboardingCandidateUpdate, OnboardingCandidateResponse

router = APIRouter(prefix="/onboardingfromsingle", tags=["OnboardingFormSingle"])

# Create candidate
@router.post("/candidate/", response_model=OnboardingCandidateResponse)
def create_candidate(payload: OnboardingCandidateCreate, db: Session = Depends(get_db)):
    db_candidate = OnboardingCandidate(**payload.dict())
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate

# Update candidate (Part A: name/email/mobile + verification options)
@router.put("/candidate/{candidate_id}", response_model=OnboardingCandidateResponse)
def update_candidate(candidate_id: int, payload: OnboardingCandidateUpdate, db: Session = Depends(get_db)):
    db_candidate = db.query(OnboardingCandidate).filter(OnboardingCandidate.id == candidate_id).first()
    if not db_candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(db_candidate, field, value)
    
    db.commit()
    db.refresh(db_candidate)
    return db_candidate

# Get candidate by ID
@router.get("/candidate/{candidate_id}", response_model=OnboardingCandidateResponse)
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    db_candidate = db.query(OnboardingCandidate).filter(OnboardingCandidate.id == candidate_id).first()
    if not db_candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return db_candidate
