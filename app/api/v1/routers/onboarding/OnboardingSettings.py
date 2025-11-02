from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.onboarding import OnboardingSetting
from app.schemas.onboarding import (
    OnboardingSettingsResponse,
    UpdateFieldRequest,
    UpdateDocumentRequest,
)

router = APIRouter(
    prefix="/onboarding/settings",
    tags=["Onboarding Settings"]
)

# ----------------- GET SETTINGS -----------------
@router.get("/", response_model=OnboardingSettingsResponse)
def get_onboarding_settings(db: Session = Depends(get_db)):
    settings = db.query(OnboardingSetting).first()
    if not settings:
        # Default values if no settings exist
        default_fields = {"presentAddress": True, "permanentAddress": True, "bankDetails": True}
        default_documents = {
            "PAN Card": True, "Adhar Card": True, "ESI Card": False, "Driving License": False,
            "Passport": False, "Voter ID": False, "Last Relieving Letter": False,
            "Last Salary Slip": False, "Latest Bank Statement": False, "Highest Education Proof": True
        }
        return {"fields": default_fields, "documents": default_documents}
    
    return {"fields": settings.fields, "documents": settings.documents}

# ----------------- UPDATE FIELD -----------------
@router.put("/field")
def update_field(request: UpdateFieldRequest, db: Session = Depends(get_db)):
    settings = db.query(OnboardingSetting).first()
    if not settings:
        settings = OnboardingSetting(fields={}, documents={})
        db.add(settings)
        db.commit()
        db.refresh(settings)
    
    settings.fields[request.field] = request.required
    db.commit()
    db.refresh(settings)
    return {"fields": settings.fields}

# ----------------- UPDATE DOCUMENT -----------------
@router.put("/document")
def update_document(request: UpdateDocumentRequest, db: Session = Depends(get_db)):
    settings = db.query(OnboardingSetting).first()
    if not settings:
        settings = OnboardingSetting(fields={}, documents={})
        db.add(settings)
        db.commit()
        db.refresh(settings)
    
    settings.documents[request.document] = request.required
    db.commit()
    db.refresh(settings)
    return {"documents": settings.documents}
