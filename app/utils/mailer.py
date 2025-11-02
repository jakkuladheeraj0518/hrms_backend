import logging
import smtplib
from email.message import EmailMessage
from typing import Optional

from app.config import settings

logger = logging.getLogger(__name__)


def _build_onboarding_message(name: str, recipient: str, form_link: str, subject: Optional[str] = None) -> EmailMessage:
    msg = EmailMessage()
    subject = subject or f"Onboarding form for {name}"
    msg["Subject"] = subject
    msg["From"] = settings.EMAIL_USER or f"no-reply@{settings.PROJECT_NAME}"
    msg["To"] = recipient
    body = (
        f"Hi {name},\n\nPlease complete the onboarding form: {form_link}\n\n"
        f"Regards,\n{settings.PROJECT_NAME}"
    )
    msg.set_content(body)
    return msg


def send_onboarding_email(name: str, recipient: str, form_link: str) -> bool:
    """Send an onboarding email using SMTP configured in settings.

    Returns True on success, False on failure. Logs exceptions.
    """
    if not settings.SMTP_SERVER or not settings.EMAIL_USER or not settings.EMAIL_PASS:
        logger.warning("SMTP not configured (SMTP_SERVER/EMAIL_USER/EMAIL_PASS missing); skipping send")
        return False

    msg = _build_onboarding_message(name, recipient, form_link)

    try:
        port = int(settings.SMTP_PORT) if settings.SMTP_PORT else 587
    except Exception:
        port = 587

    try:
        with smtplib.SMTP(settings.SMTP_SERVER, port, timeout=30) as smtp:
            smtp.ehlo()
            # Use STARTTLS for port 587
            try:
                smtp.starttls()
                smtp.ehlo()
            except Exception:
                # Some servers may not require STARTTLS; continue if starttls fails
                logger.debug("STARTTLS negotiation failed or not supported; continuing without it")

            smtp.login(settings.EMAIL_USER, settings.EMAIL_PASS)
            smtp.send_message(msg)

        logger.info("Email sent to %s", recipient)
        return True
    except Exception as exc:
        logger.exception("Failed to send email to %s: %s", recipient, exc)
        return False
