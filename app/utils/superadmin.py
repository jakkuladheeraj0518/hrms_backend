from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import jwt
from app.config import settings
import random
import string

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def generate_invoice_id() -> str:
    """Generate unique invoice ID"""
    timestamp = datetime.now().strftime("%Y%m%d")
    random_suffix = ''.join(random.choices(string.digits, k=4))
    return f"INV{timestamp}{random_suffix}"

def calculate_expiry_date(
    billing_cycle: str,
    start_date: Optional[datetime] = None
) -> datetime:
    """Calculate subscription expiry date based on billing cycle"""
    if start_date is None:
        start_date = datetime.utcnow()
    
    if "30 Days" in billing_cycle or "Monthly" in billing_cycle:
        return start_date + timedelta(days=30)
    elif "365 Days" in billing_cycle or "Yearly" in billing_cycle:
        return start_date + timedelta(days=365)
    else:
        # Default to 30 days
        return start_date + timedelta(days=30)

def format_currency(amount: float, currency: str = "USD") -> str:
    """Format amount with currency symbol"""
    symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "INR": "₹"
    }
    symbol = symbols.get(currency, currency)
    return f"{symbol}{amount:,.2f}"