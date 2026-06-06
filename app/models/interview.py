from sqlalchemy import (
    Column, Integer, String, Text,
    DateTime, ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )
    job_id = Column(
        Integer, ForeignKey("jobs.id"), nullable=False, index=True
    )
    start_time = Column(DateTime(timezone=True), nullable=True)
    end_time = Column(DateTime(timezone=True), nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    overall_score = Column(Integer, nullable=True)
    communication_score = Column(Integer, nullable=True)
    technical_score = Column(Integer, nullable=True)
    status = Column(String(50), default="in-progress")
    feedback_text = Column(Text, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Relationships
    user = relationship("User", back_populates="interviews")
    job = relationship("Job", back_populates="interviews")
    questions = relationship(
        "Question",
        back_populates="interview",
        cascade="all, delete-orphan"
    )
    job_applications = relationship(
        "JobApplication", back_populates="interview"
    )


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(
        Integer, ForeignKey("interviews.id"), nullable=False, index=True
    )
    question_text = Column(Text, nullable=False)
    category = Column(String(100), default="general")
    difficulty = Column(Integer, default=1)
    expected_duration_seconds = Column(Integer, default=120)
    question_order = Column(Integer, default=1)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Relationships
    interview = relationship("Interview", back_populates="questions")
    answers = relationship(
        "Answer",
        back_populates="question",
        cascade="all, delete-orphan"
    )


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(
        Integer, ForeignKey("questions.id"), nullable=False, index=True
    )
    user_id = Column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )
    answer_text = Column(Text, nullable=False)
    duration_seconds = Column(Integer, nullable=True)
    score = Column(Integer, nullable=True)
    feedback = Column(Text, nullable=True)
    submitted_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Relationships
    question = relationship("Question", back_populates="answers")
    user = relationship("User", back_populates="answers")
