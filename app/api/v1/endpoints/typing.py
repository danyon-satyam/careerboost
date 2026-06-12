from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.database import get_db
from app.core.security import get_current_user_id
from app.schemas.typing import (
    TypingTestRequest,
    TypingSubmit,
    TypingResult,
    TypingResultDetail
)
from app.models.typing_session import TypingSession
from app.services.typing_metrics import typing_metrics_service

router = APIRouter(prefix="/typing", tags=["Typing Practice"])


@router.get(
    "/test",
    summary="Get a typing test text"
)
def get_test_text(
    difficulty: str = Query(
        default="medium",
        description="easy, medium, hard, or code"
    )
):
    """
    Get a random typing test text for the given difficulty.

    Difficulty levels:
    - **easy**: simple sentences, common words
    - **medium**: professional and technical paragraphs
    - **hard**: complex technical content
    - **code**: actual Python code snippets
    """
    text = typing_metrics_service.get_test_text(difficulty)
    return {
        "text": text,
        "difficulty": difficulty,
        "word_count": len(text.split()),
        "char_count": len(text)
    }


@router.post(
    "/submit",
    response_model=TypingResultDetail,
    status_code=201,
    summary="Submit typing test results"
)
def submit_typing_result(
    payload: TypingSubmit,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Submit a completed typing test and get performance metrics.

    - Calculates WPM, accuracy, and error count
    - Saves session to history
    - Returns detailed performance report
    """
    metrics = typing_metrics_service.calculate_metrics(
        test_text=payload.test_text,
        submitted_text=payload.submitted_text,
        time_taken_seconds=payload.time_taken_seconds
    )

    session = TypingSession(
        user_id=current_user_id,
        test_text=payload.test_text,
        submitted_text=payload.submitted_text,
        wpm=metrics["wpm"],
        accuracy_percentage=metrics["accuracy_percentage"],
        errors_count=metrics["errors_count"],
        time_taken_seconds=payload.time_taken_seconds
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    return TypingResultDetail(
        id=session.id,
        wpm=session.wpm,
        accuracy_percentage=session.accuracy_percentage,
        errors_count=session.errors_count,
        time_taken_seconds=session.time_taken_seconds,
        performance_level=metrics["performance_level"],
        feedback=metrics["feedback"],
        created_at=session.created_at
    )


@router.get(
    "/history",
    response_model=List[TypingResult],
    summary="Get typing session history"
)
def get_typing_history(
    limit: int = Query(default=10, ge=1, le=50),
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get the user's recent typing practice sessions."""
    sessions = db.query(TypingSession).filter(
        TypingSession.user_id == current_user_id
    ).order_by(
        TypingSession.created_at.desc()
    ).limit(limit).all()
    return sessions


@router.get(
    "/progress",
    summary="Get typing progress statistics"
)
def get_typing_progress(
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Get aggregated typing progress across all sessions.
    Shows average WPM, best WPM, accuracy trend, and improvement.
    """
    sessions = db.query(TypingSession).filter(
        TypingSession.user_id == current_user_id
    ).order_by(TypingSession.created_at.asc()).all()

    session_data = [
        {
            "wpm": s.wpm,
            "accuracy_percentage": s.accuracy_percentage
        }
        for s in sessions
    ]

    return typing_metrics_service.calculate_progress(session_data)
