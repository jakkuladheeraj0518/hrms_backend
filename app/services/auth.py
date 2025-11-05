from datetime import timedelta, datetime
from typing import Optional
from fastapi import HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
import jwt

from app.repositories.auth import UserRepository
from app.schemas.auth import UserCreate, UserLogin, LoginResponse, UserResponse
from app.utils.auth import verify_password, create_access_token, get_password_hash
from app.config import settings


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
    
    def register_user(self, user_in: UserCreate) -> UserResponse:
        """Register a new user"""
        existing_user = self.user_repo.get_by_email(user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        user = self.user_repo.create(user_in)
        return UserResponse.model_validate(user)
    
    def authenticate_user(self, login_data: UserLogin) -> LoginResponse:
        """Authenticate user and return token"""
        user = self.user_repo.get_by_email(login_data.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        if not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        if getattr(login_data, "remember", False):
            access_token_expires = timedelta(days=30)
        
        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=access_token_expires
        )
        
        self.user_repo.update_last_login(user)
        
        return LoginResponse(
            user=UserResponse.model_validate(user),
            access_token=access_token,
            token_type="bearer"
        )
    
    def get_current_user(self, email: str) -> Optional[UserResponse]:
        """Get current user by email"""
        user = self.user_repo.get_by_email(email)
        if not user:
            return None
        return UserResponse.model_validate(user)

    # ---------------------------------------------------------
    # 🔐 Forgot Password & Reset Password
    # ---------------------------------------------------------
    
    def initiate_password_reset(self, email: str, background_tasks: BackgroundTasks):
        """Generate a password reset token and send it via email"""
        user = self.user_repo.get_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        token_data = {
            "sub": user.email,
            "exp": datetime.utcnow() + timedelta(minutes=15)
        }
        token = jwt.encode(token_data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        # In production, replace this print with a real email sender.
        reset_link = f"http://localhost:8000/reset-password?token={token}"
        print(f"🔗 Password reset link for {email}: {reset_link}")

        # Optionally send via email asynchronously
        # background_tasks.add_task(send_email, email, reset_link)

        return {"message": "Password reset link sent to your email"}

    def reset_password(self, token: str, new_password: str):
        """Verify reset token and update user's password"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            email = payload.get("sub")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=400, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=400, detail="Invalid token")

        user = self.user_repo.get_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.hashed_password = get_password_hash(new_password)
        self.db.commit()
        return {"message": "Password has been reset successfully"}
