from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, TokenResponse
from app.services.user_service import user_service
from app.core.security import verify_password, create_access_token
from app.core.exceptions import UnauthorizedError

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=201,
    summary="Create a new user account"
)
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    - **email**: valid email address (must be unique)
    - **password**: minimum 6 characters
    - **full_name**: candidate's full name
    """
    user = user_service.create_user(
        db=db,
        email=payload.email,
        password=payload.password,
        full_name=payload.full_name
    )
    return user


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login and get JWT token"
)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate a user and return a JWT access token.
    - **email**: registered email
    - **password**: account password
    """
    user = user_service.get_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.password_hash):
        raise UnauthorizedError("Invalid email or password")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
