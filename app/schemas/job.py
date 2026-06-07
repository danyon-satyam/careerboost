from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime


class JobCreate(BaseModel):
    title: str
    company: str
    description: str
    required_skills: List[str] = []
    required_experience: int = 0
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    location: Optional[str] = None
    job_type: str = "full-time"
    source: str = "manual"

    @field_validator("title", "company", "description")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()

    @field_validator("job_type")
    @classmethod
    def valid_job_type(cls, v: str) -> str:
        allowed = ["full-time", "part-time", "remote", "contract", "internship"]
        if v not in allowed:
            raise ValueError(f"job_type must be one of {allowed}")
        return v


class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    description: str
    required_skills: List[str] = []
    required_experience: int
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    location: Optional[str] = None
    job_type: str
    source: str
    is_active: bool
    posted_date: datetime
    created_at: datetime

    model_config = {"from_attributes": True}


class JobListResponse(BaseModel):
    jobs: List[JobResponse]
    total: int
    page: int
    page_size: int


class JobSearchResponse(BaseModel):
    jobs: List[JobResponse]
    total: int
    query: str
