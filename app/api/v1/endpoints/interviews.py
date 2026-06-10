from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.core.security import get_current_user_id
from app.schemas.interview import (
    InterviewStart,
    InterviewResponse,
    InterviewSummary,
    AnswerSubmit,
    AnswerResponse,
    InterviewResultResponse
)
from app.services.interview_service import interview_service
from app.services.conversation_service import conversation_service


router = APIRouter(prefix="/interviews", tags=["Interviews"])


@router.post(
    "/start",
    response_model=InterviewResponse,
    status_code=201,
    summary="Start a new AI mock interview"
)
def start_interview(
    payload: InterviewStart,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Start a new mock interview for a specific job.

    - Creates interview session linked to user + job
    - Generates interview questions
    - Week 2: questions will be AI-generated from resume + JD
    - Returns interview object with all questions

    Candidate speaks answers — use Web Speech API on frontend
    to capture voice and send transcript text to submit-answer.
    """
    return interview_service.start_interview(
        db=db,
        user_id=current_user_id,
        job_id=payload.job_id
    )


@router.get(
    "",
    response_model=List[InterviewSummary],
    summary="List all interviews for current user"
)
def list_interviews(
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get all past and ongoing interviews for the logged-in user."""
    return interview_service.get_user_interviews(
        db=db,
        user_id=current_user_id
    )


@router.get(
    "/{interview_id}",
    response_model=InterviewResponse,
    summary="Get interview details"
)
def get_interview(
    interview_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get full details of a specific interview including questions."""
    return interview_service.get_by_id(
        db=db,
        interview_id=interview_id,
        user_id=current_user_id
    )


@router.post(
    "/{interview_id}/submit-answer",
    response_model=AnswerResponse,
    summary="Submit a spoken answer"
)
def submit_answer(
    interview_id: int,
    payload: AnswerSubmit,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Submit a candidate's spoken answer for evaluation.

    The answer_text should be the transcript from the browser's
    Web Speech API after the candidate speaks their response.

    - Evaluates answer quality
    - Returns score (0-100) and feedback
    - Week 2: AI evaluation via Gemini + spaCy
    """
    return interview_service.submit_answer(
        db=db,
        interview_id=interview_id,
        user_id=current_user_id,
        question_id=payload.question_id,
        answer_text=payload.answer_text,
        duration_seconds=payload.duration_seconds
    )


@router.post(
    "/{interview_id}/end",
    response_model=InterviewSummary,
    summary="End the interview session"
)
def end_interview(
    interview_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    End the interview and calculate final scores.
    Sets status to 'completed' and generates overall feedback.
    """
    return interview_service.end_interview(
        db=db,
        interview_id=interview_id,
        user_id=current_user_id
    )


@router.get(
    "/{interview_id}/results",
    response_model=InterviewResultResponse,
    summary="Get interview results and scores"
)
def get_results(
    interview_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Get the full results of a completed interview.

    Returns:
    - Overall score (0-100)
    - Technical and communication scores
    - Detailed feedback text
    - Questions answered vs total
    """
    return interview_service.get_results(
        db=db,
        interview_id=interview_id,
        user_id=current_user_id
    )


@router.get(
    "/{interview_id}/next-question",
    summary="Get next question with conversation context"
)
def get_next_question(
    interview_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Get the next unanswered question with conversation context.

    Returns:
    - The next question to ask
    - A natural transition message
    - Progress (current/total questions)
    - Or interview_complete=True if all questions answered
    """
    return conversation_service.get_next_question(
        db=db,
        interview_id=interview_id,
        user_id=current_user_id
    )


@router.post(
    "/{interview_id}/process-answer",
    summary="Process spoken answer with full AI conversation flow"
)
def process_answer(
    interview_id: int,
    payload: AnswerSubmit,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Process a spoken answer through the full conversation pipeline.

    Unlike submit-answer (which just saves), this endpoint:
    - Evaluates with full AI pipeline
    - Generates follow-up if answer needs clarification
    - Returns conversation response message
    - Handles the natural interview flow

    Use this endpoint for the live interview UI.
    Use submit-answer for simple answer recording.
    """
    return conversation_service.process_answer(
        db=db,
        interview_id=interview_id,
        user_id=current_user_id,
        question_id=payload.question_id,
        answer_text=payload.answer_text,
        duration_seconds=payload.duration_seconds
    )


@router.get(
    "/{interview_id}/greeting",
    summary="Get personalized AI interview greeting"
)
def get_greeting(
    interview_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Get a personalized greeting to start the interview.
    Called once when the candidate enters the live interview room.
    """
    from app.services.user_service import user_service

    interview = interview_service.get_by_id(
        db, interview_id, current_user_id
    )
    user = user_service.get_by_id(db, current_user_id)

    total_questions = len(interview.questions)
    job_title = interview.job.title if interview.job else "this role"

    greeting = conversation_service.get_interview_greeting(
        job_title=job_title,
        candidate_name=user.full_name,
        total_questions=total_questions
    )

    return {
        "greeting": greeting,
        "interview_id": interview_id,
        "job_title": job_title,
        "total_questions": total_questions
    }
