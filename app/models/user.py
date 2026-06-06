from sqlalchemy import (
    Column, Integer, String, Float,
    JSON, Text, DateTime, Boolean
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    resume_text = Column(Text, nullable=True)
    profile_summary = Column(Text, nullable=True)
    skills = Column(JSON, default=list)
    experience_years = Column(Float, default=0.0)
    current_position = Column(String(255), nullable=True)
    target_role = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )

    # Relationships
    interviews = relationship(
        "Interview", back_populates="user", cascade="all, delete-orphan"
    )
    answers = relationship(
        "Answer", back_populates="user", cascade="all, delete-orphan"
    )
    typing_sessions = relationship(
        "TypingSession", back_populates="user", cascade="all, delete-orphan"
    )
    job_applications = relationship(
        "JobApplication", back_populates="user", cascade="all, delete-orphan"
    )
