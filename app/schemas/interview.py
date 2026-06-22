from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime


class InterviewStart(BaseModel):
    job_id: int


class QuestionResponse(BaseModel):
    id: int
    question_text: str
    category: str
    difficulty: int
    question_order: int
    expected_duration_seconds: int

    model_config = {"from_attributes": True}


class InterviewResponse(BaseModel):
    id: int
    user_id: int
    job_id: int
    status: str
    overall_score: Optional[int] = None
    communication_score: Optional[int] = None
    technical_score: Optional[int] = None
    feedback_text: Optional[str] = None
    created_at: datetime
    questions: List[QuestionResponse] = []

    model_config = {"from_attributes": True}


class InterviewSummary(BaseModel):
    id: int
    job_id: int
    status: str
    overall_score: Optional[int] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class AnswerSubmit(BaseModel):
    question_id: int
    answer_text: str
    duration_seconds: Optional[int] = None

    @field_validator("answer_text")
    @classmethod
    def answer_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Answer cannot be empty")
        return v.strip()


class AnswerResponse(BaseModel):
    id: int
    question_id: int
    answer_text: str
    score: Optional[int] = None
    feedback: Optional[str] = None
    duration_seconds: Optional[int] = None
    submitted_at: datetime

    model_config = {"from_attributes": True}


class InterviewResultResponse(BaseModel):
    id: int
    status: str
    overall_score: Optional[int] = None
    communication_score: Optional[int] = None
    technical_score: Optional[int] = None
    feedback_text: Optional[str] = None
    total_questions: int
    answered_questions: int

    model_config = {"from_attributes": True}


class JDParseRequest(BaseModel):
    jd_text: str
    title: Optional[str] = None
    company: Optional[str] = None

    @field_validator("jd_text")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if len(v.strip()) < 50:
            raise ValueError(
                "Job description must be at least 50 characters"
            )
        return v.strip()


class JDParseResponse(BaseModel):
    interview_id: int
    job_id: int
    title: str
    company: str
    extracted_skills: List[str]
    required_experience: int
    questions: List[QuestionResponse]
    total_questions: int
    sections: List[str]
    status: str
