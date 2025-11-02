from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.onboarding import BulkOnboardingRequest, BulkCandidateResponse
from app.models.onboarding import BulkCandidate, CreditTransaction
from app.utils.mailer import send_onboarding_email
from datetime import datetime
from app.config import settings

router = APIRouter(prefix="/api/bulkonboarding", tags=["Bulk Onboarding"])

# POST Bulk Onboarding
@router.post("/send", response_model=List[BulkCandidateResponse])
def send_bulk_onboarding(request: BulkOnboardingRequest, db: Session = Depends(get_db)):
    candidates_data = request.candidates
    verification = request.verification_options
    credits = request.credits

    if not candidates_data:
        raise HTTPException(status_code=400, detail="No candidates provided")

    total_required = 0
    if verification.pan:
        total_required += 5
    if verification.bank:
        total_required += 5
    if verification.aadhar:
        total_required += 5

    if credits < total_required:
        raise HTTPException(status_code=400, detail=f"Insufficient credits. Need {total_required}, have {credits}.")

    added_candidates = []
    for cand in candidates_data:
        new_cand = BulkCandidate(
            name=cand.name,
            email=cand.email,
            mobile=cand.mobile,
            status="Form Sent",
            created_at=datetime.utcnow()
        )
        db.add(new_cand)
        added_candidates.append(new_cand)

        # Build form link from frontend URL (if configured), and call mailer.
        frontend = getattr(settings, "FRONTEND_URL", "http://yourfrontend.com").rstrip('/')
        form_link = f"{frontend}/onboarding/form"
        # mailer expects (name, recipient, form_link)
        send_onboarding_email(cand.name, cand.email, form_link)

    if total_required > 0:
        transaction = CreditTransaction(
            used_credits=total_required,
            purpose="Bulk Onboarding Verification",
            created_at=datetime.utcnow()
        )
        db.add(transaction)

    db.commit()
    return added_candidates

# GET all Bulk Candidates
@router.get("/list", response_model=List[BulkCandidateResponse])
def get_bulk_candidates(db: Session = Depends(get_db)):
    candidates = db.query(BulkCandidate).order_by(BulkCandidate.created_at.desc()).all()
    return candidates
