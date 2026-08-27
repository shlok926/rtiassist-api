from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timezone
from models.orm.user import User
from models.schemas import UserRegisterRequest, UserLoginRequest, TokenResponse, UserProfileResponse
from utils.security import get_password_hash, verify_password, create_access_token
from models.database import get_db

def register_user(db: Session, request: UserRegisterRequest) -> UserProfileResponse:
    email = request.email.strip().lower()
    
    if not email:
        raise HTTPException(status_code=400, detail="Email is required.")
        
    if len(request.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters.")
        
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")
        
    user = User(
        email=email,
        password_hash=get_password_hash(request.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return UserProfileResponse.model_validate(user)

def login_user(db: Session, request: UserLoginRequest) -> TokenResponse:
    email = request.email.strip().lower()
    
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.password_hash:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")
        
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")
        
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user account.")
        
    user.last_login_at = datetime.now(timezone.utc)
    db.commit()
    
    access_token = create_access_token(subject=user.id)
    return TokenResponse(access_token=access_token)

def get_user_profile(user: User) -> UserProfileResponse:
    return UserProfileResponse.model_validate(user)
