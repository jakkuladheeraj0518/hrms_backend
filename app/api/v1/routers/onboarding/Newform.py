import os
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.onboarding import OnboardingForm
from app.schemas.onboarding import OnboardingFormResponse

# Directory to store uploaded files
UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/newform", tags=["New Form"])

# ------------------------------------------------------
# 1️⃣ Create or Update Onboarding Form with Two Files
# ------------------------------------------------------
@router.post("/", response_model=OnboardingFormResponse)
async def create_or_update_form(
    candidate_name: str = Form(...),
    candidate_email: str = Form(...),
    candidate_phone: str = Form(...),
    policies_file: UploadFile = File(None),
    offer_letter_file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    """
    This endpoint handles:
      - Candidate Details (Part A)
      - Upload Policies file (Part B)
      - Upload Offer Letter file (Part C)
    """

    new_form = OnboardingForm(
        candidate_name=candidate_name,
        candidate_email=candidate_email,
        candidate_phone=candidate_phone,
        finalized=False
    )

    # Handle Policies file upload
    if policies_file:
        policies_path = os.path.join(UPLOAD_DIR, f"policies_{policies_file.filename}")
        with open(policies_path, "wb") as f:
            f.write(await policies_file.read())
        new_form.policies = policies_path
    else:
        new_form.policies = "No policies file uploaded"

    # Handle Offer Letter file upload
    if offer_letter_file:
        offer_path = os.path.join(UPLOAD_DIR, f"offerletter_{offer_letter_file.filename}")
        with open(offer_path, "wb") as f:
            f.write(await offer_letter_file.read())
        new_form.offer_letter = offer_path
    else:
        new_form.offer_letter = "No offer letter file uploaded"

    db.add(new_form)
    db.commit()
    db.refresh(new_form)

    return new_form


# ------------------------------------------------------
# 2️⃣ Get Form by ID (View in React or Swagger)
# ------------------------------------------------------
@router.get("/{form_id}", response_model=OnboardingFormResponse)
def get_form(form_id: int, db: Session = Depends(get_db)):
    form = db.query(OnboardingForm).filter(OnboardingForm.id == form_id).first()
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")
    return form


# ------------------------------------------------------
# 3️⃣ Finalize Form (Mark as Completed)
# ------------------------------------------------------
@router.post("/{form_id}/finalize", response_model=OnboardingFormResponse)
def finalize_form(form_id: int, db: Session = Depends(get_db)):
    form = db.query(OnboardingForm).filter(OnboardingForm.id == form_id).first()
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")

    form.finalized = True
    db.commit()
    db.refresh(form)
    return form
