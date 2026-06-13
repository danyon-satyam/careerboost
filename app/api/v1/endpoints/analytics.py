from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.security import get_current_user_id
from app.services.analytics_service import analytics_service

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get(
    "/dashboard",
    summary="Get dashboard summary"
)
def get_dashboard(
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Get a complete dashboard summary including interview stats,
    typing stats, application stats, and an overall readiness score.
    """
    return analytics_service.get_dashboard_summary(
        db=db, user_id=current_user_id
    )


@router.get(
    "/interviews",
    summary="Get interview performance analytics"
)
def get_interview_analytics(
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Get detailed interview analytics: score trends,
    category breakdown (behavioral/technical/general),
    and performance trend (improving/stable/declining).
    """
    return analytics_service.get_interview_analytics(
        db=db, user_id=current_user_id
    )


@router.get(
    "/typing",
    summary="Get typing performance analytics"
)
def get_typing_analytics(
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Get detailed typing analytics: WPM trend over time,
    average and best WPM, average accuracy.
    """
    return analytics_service.get_typing_analytics(
        db=db, user_id=current_user_id
    )
