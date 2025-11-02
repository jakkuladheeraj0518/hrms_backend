from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging
from app.database.session import get_db
from app.models.onboarding import FinalizedForm
from app.schemas.onboarding import FinalizeRequest
from app.utils.mailer import send_onboarding_email as send_email
from app.utils.sms import send_sms
from app.config import settings
from datetime import datetime


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/onboarding/finalize",
    tags=["Finalize and Send Form"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def finalize_and_send_form(request: FinalizeRequest, db: Session = Depends(get_db)):
    """
    Finalize the onboarding form and optionally send email/SMS.
    """
    try:
        # Create new finalized record
        new_form = FinalizedForm(
            candidate_name=request.candidate_name,
            candidate_email=request.candidate_email,
            candidate_phone=request.candidate_phone,
            send_form=request.send_form,
            status="sent" if request.send_form else "saved",
            finalized_at=datetime.utcnow()
        )

        db.add(new_form)
        db.commit()
        db.refresh(new_form)

        message = "Form finalized but not sent."

        # Send notifications if send_form is True
        if request.send_form:
            frontend = getattr(settings, "FRONTEND_URL", "http://yourfrontend.com").rstrip('/')
            form_link = f"{frontend}/onboarding/form/{new_form.id}"

            # Use provided recipient values or fall back to defaults from settings
            recipient_email = new_form.candidate_email or getattr(settings, "DEFAULT_RECIPIENT_EMAIL", None)
            recipient_phone = new_form.candidate_phone or getattr(settings, "DEFAULT_RECIPIENT_MOBILE", None)

            email_ok = False
            sms_ok = False

            if recipient_email:
                email_ok = send_email(
                    new_form.candidate_name,
                    recipient_email,
                    form_link
                )

            if recipient_phone:
                # sms.send_sms expects (to_number, message)
                sms_ok = send_sms(
                    recipient_phone,
                    f"Hi {new_form.candidate_name}, please complete your onboarding form: {form_link}"
                )

            if email_ok or sms_ok:
                message = f"✅ Onboarding form sent to {recipient_email} and {recipient_phone}"
            else:
                raise HTTPException(status_code=500, detail="Failed to send email or SMS")

        return {"message": message, "form_data": new_form}

    except Exception as e:
        logger.exception("Error finalizing form: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", status_code=status.HTTP_200_OK)
def get_all_finalized_forms(db: Session = Depends(get_db)):
    """
    Retrieve all finalized onboarding forms.
    """
    forms = db.query(FinalizedForm).all()
    if not forms:
        raise HTTPException(status_code=404, detail="No finalized forms found.")
    return forms
