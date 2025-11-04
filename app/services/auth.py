from datetime import timedelta
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.auth import UserRepository
from app.schemas.auth import UserCreate, UserLogin, LoginResponse, UserResponse
from app.utils.auth import verify_password, create_access_token
from app.config import settings

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
    
    def register_user(self, user_in: UserCreate) -> UserResponse:
        """Register a new user"""
        # Check if user already exists
        existing_user = self.user_repo.get_by_email(user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        user = self.user_repo.create(user_in)
        return UserResponse.model_validate(user)
    
    def authenticate_user(self, login_data: UserLogin) -> LoginResponse:
        """Authenticate user and return token"""
        # Get user by email
        user = self.user_repo.get_by_email(login_data.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Verify password
        if not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        if login_data.remember:
            access_token_expires = timedelta(days=30)
        
        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=access_token_expires
        )
        
        # Update last login
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