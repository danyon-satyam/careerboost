from sqlalchemy import (
    Column, Integer, String, Text,
    Float, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class TypingSession(Base):
    __tablename__ = "typing_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )
    test_text = Column(Text, nullable=False)
    submitted_text = Column(Text, nullable=True)
    wpm = Column(Float, nullable=True)
    accuracy_percentage = Column(Float, nullable=True)
    time_taken_seconds = Column(Integer, nullable=True)
    errors_count = Column(Integer, default=0)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Relationships
    user = relationship("User", back_populates="typing_sessions")


class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )
    job_id = Column(
        Integer, ForeignKey("jobs.id"), nullable=False, index=True
    )
    interview_id = Column(
        Integer, ForeignKey("interviews.id"), nullable=True
    )
    status = Column(String(50), default="applied")
    applied_date = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    last_updated = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )

    # Relationships
    user = relationship("User", back_populates="job_applications")
    job = relationship("Job", back_populates="job_applications")
    interview = relationship("Interview", back_populates="job_applications")