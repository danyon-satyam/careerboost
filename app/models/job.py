from sqlalchemy import (
    Column, Integer, String, Text,
    JSON, Boolean, DateTime, Float
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    company = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    required_skills = Column(JSON, default=list)
    required_experience = Column(Integer, default=0)
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    location = Column(String(255), nullable=True, index=True)
    job_type = Column(String(50), default="full-time")
    source = Column(String(100), default="manual")
    is_active = Column(Boolean, default=True)
    application_deadline = Column(DateTime(timezone=True), nullable=True)
    posted_date = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Relationships
    interviews = relationship("Interview", back_populates="job")
    job_applications = relationship(
        "JobApplication", back_populates="job"
    )