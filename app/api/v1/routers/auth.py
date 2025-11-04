from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.auth import UserCreate, UserLogin, LoginResponse, UserResponse
from app.services.auth import AuthService
from app.dependencies.auth import get_current_active_user

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

@router.post("/logout")
def logout(
    current_user: UserResponse = Depends(get_current_active_user)
):
    """
    Logout user (client should remove token)
    """
    return {"message": "Successfully logged out"}