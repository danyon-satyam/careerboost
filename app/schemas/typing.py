from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


class TypingTestRequest(BaseModel):
    difficulty: str = "medium"

    @field_validator("difficulty")
    @classmethod
    def valid_difficulty(cls, v: str) -> str:
        allowed = ["easy", "medium", "hard", "code"]
        if v not in allowed:
            raise ValueError(
                f"difficulty must be one of {allowed}"
            )
        return v


class TypingSubmit(BaseModel):
    test_text: str
    submitted_text: str
    time_taken_seconds: int

    @field_validator("time_taken_seconds")
    @classmethod
    def positive_time(cls, v: int) -> int:
        if v <= 0:
            raise ValueError(
                "time_taken_seconds must be positive"
            )
        return v

    @field_validator("submitted_text")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("submitted_text cannot be empty")
        return v


class TypingResult(BaseModel):
    id: int
    wpm: Optional[float] = None
    accuracy_percentage: Optional[float] = None
    errors_count: int
    time_taken_seconds: Optional[int] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class TypingResultDetail(BaseModel):
    id: int
    wpm: Optional[float] = None
    accuracy_percentage: Optional[float] = None
    errors_count: int
    time_taken_seconds: Optional[int] = None
    performance_level: Optional[str] = None
    feedback: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}
