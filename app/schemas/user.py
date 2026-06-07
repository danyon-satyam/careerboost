from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v

    @field_validator("full_name")
    @classmethod
    def full_name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Full name cannot be empty")
        return v.strip()


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    profile_summary: Optional[str] = None
    skills: Optional[List[str]] = None
    experience_years: Optional[float] = None
    current_position: Optional[str] = None
    target_role: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    profile_summary: Optional[str] = None
    skills: List[str] = []
    experience_years: float = 0.0
    current_position: Optional[str] = None
    target_role: Optional[str] = None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
