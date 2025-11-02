import logging
from app.config import settings

logger = logging.getLogger(__name__)

def send_sms(to_number: str, message: str) -> bool:
    logger.info("Mock SMS to %s: %s", to_number, message)
    return True
