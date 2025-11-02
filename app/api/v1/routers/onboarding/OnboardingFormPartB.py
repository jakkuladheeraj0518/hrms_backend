from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database.session import get_db
from app.models.onboarding import OnboardingCandidate
from app.schemas.onboarding import OnboardingCandidateResponse

router = APIRouter(
    prefix="/onboarding/form/partb",
    tags=["Onboarding Form Part B"]
)

# ✅ Get candidate details by ID (to display candidate summary)
@router.get("/{candidate_id}", response_model=OnboardingCandidateResponse)
def get_candidate_partb(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.query(OnboardingCandidate).filter(OnboardingCandidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate


# ✅ Update Part B - Attach Policies (and mark as attached)
@router.put("/{candidate_id}/attach-policies", response_model=OnboardingCandidateResponse)
def attach_policies(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.query(OnboardingCandidate).filter(OnboardingCandidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    candidate.policies_attached = True
    candidate.form_status = "Policies Attached"
    candidate.finalized_at = datetime.utcnow()

    db.commit()
    db.refresh(candidate)
    return candidate
