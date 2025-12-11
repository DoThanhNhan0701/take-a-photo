from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_tokens, verify_token
from app.core.deps import get_current_user
from app.schemas import user as user_schemas
from app.crud import user as user_crud
from app.models.user import User
import uuid

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login", response_model=user_schemas.Token)
def login(credentials: user_schemas.UserLogin, db: Session = Depends(get_db)):
    """Authenticate a user and return access and refresh tokens"""
    user = user_crud.authenticate_user(db, username=credentials.username, password=credentials.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    
    # Update last login
    user_crud.update_last_login(db, user_id=user.id)
    
    # Create and return tokens
    tokens = create_tokens(user_id=user.id, username=user.username)
    return tokens


@router.post("/refresh", response_model=user_schemas.Token)
def refresh_access_token(refresh_request: user_schemas.RefreshTokenRequest, db: Session = Depends(get_db)):
    """Refresh access token using refresh token"""
    # Verify refresh token
    payload = verify_token(refresh_request.refresh_token, token_type="refresh")
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = uuid.UUID(payload.get("sub"))
    username = payload.get("username")
    
    # Verify user still exists
    user = user_crud.get_user(db, user_id=user_id)
    if user is None or user.username != username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or username mismatch"
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    
    # Create and return new tokens
    tokens = create_tokens(user_id=user.id, username=user.username)
    return tokens


@router.get("/me", response_model=user_schemas.UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current authenticated user information"""
    return current_user


@router.put("/me", response_model=user_schemas.UserResponse)
def update_current_user_info(
    user_update: user_schemas.UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current authenticated user information"""
    # Don't allow changing username via this endpoint
    if user_update.username and user_update.username != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change username via this endpoint"
        )
    
    updated_user = user_crud.update_user(db, user_id=current_user.id, user=user_update)
    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return updated_user
