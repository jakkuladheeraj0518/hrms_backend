from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.auth import UserCreate, UserLogin, LoginResponse, UserResponse
from app.services.auth import AuthService
from app.dependencies.auth import get_current_active_user
from fastapi import BackgroundTasks
from app.schemas.auth import ForgotPasswordRequest, ResetPasswordRequest
from app.services.auth import AuthService

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user
    """
    auth_service = AuthService(db)
    return auth_service.register_user(user_in)

@router.post("/login", response_model=LoginResponse)
def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login user and return access token
    """
    auth_service = AuthService(db)
    return auth_service.authenticate_user(login_data)

@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: UserResponse = Depends(get_current_active_user)
):
    """
    Get current user information
    """
    return current_user

@router.post("/forgot-password")
def forgot_password(
    request: ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Generate a password reset token and send it via email.
    """
    auth_service = AuthService(db)
    return auth_service.initiate_password_reset(request.email, background_tasks)


@router.post("/reset-password")
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Reset password using the token sent to email.
    """
    auth_service = AuthService(db)
    return auth_service.reset_password(request.token, request.new_password)

@router.post("/logout")
def logout(
    current_user: UserResponse = Depends(get_current_active_user)
):
    """
    Logout user (client should remove token)
    """
    return {"message": "Successfully logged out"}
