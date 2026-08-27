from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.database import get_db
from models.schemas import UserRegisterRequest, UserLoginRequest, TokenResponse, UserProfileResponse
from services import auth_service
from dependencies.auth import get_current_user
from models.orm.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserProfileResponse)
def register(request: UserRegisterRequest, db: Session = Depends(get_db)):
    return auth_service.register_user(db, request)

@router.post("/login", response_model=TokenResponse)
def login(request: UserLoginRequest, db: Session = Depends(get_db)):
    return auth_service.login_user(db, request)

@router.get("/me", response_model=UserProfileResponse)
def me(current_user: User = Depends(get_current_user)):
    return auth_service.get_user_profile(current_user)

@router.post("/logout")
def logout():
    # Since we are using stateless JWT, logout is handled client-side by deleting the token.
    return {"message": "Successfully logged out client-side."}

from dependencies.auth import get_admin_user

@router.get("/admin-only")
def admin_only(admin_user: User = Depends(get_admin_user)):
    return {"message": f"Welcome, admin {admin_user.email}"}
