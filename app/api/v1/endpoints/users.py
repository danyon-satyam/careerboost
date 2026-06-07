from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.security import get_current_user_id
from app.schemas.user import UserResponse, UserUpdate
from app.services.user_service import user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/profile",
    response_model=UserResponse,
    summary="Get current user profile"
)
def get_profile(
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Get the authenticated user's profile.
    Requires a valid JWT token in the Authorization header.
    """
    return user_service.get_by_id(db, current_user_id)


@router.patch(
    "/profile",
    response_model=UserResponse,
    summary="Update current user profile"
)
def update_profile(
    payload: UserUpdate,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Update the authenticated user's profile fields.
    Only provided fields are updated — others remain unchanged.
    """
    update_data = payload.model_dump(exclude_none=True)
    return user_service.update_user(db, current_user_id, update_data)


@router.get(
    "/stats",
    summary="Get user statistics"
)
def get_user_stats(
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Get interview and typing statistics for the authenticated user.
    Full implementation in Week 3 analytics module.
    """
    user = user_service.get_by_id(db, current_user_id)
    return {
        "user_id": user.id,
        "total_interviews": len(user.interviews),
        "total_typing_sessions": len(user.typing_sessions),
        "total_applications": len(user.job_applications),
        "skills_count": len(user.skills or []),
    }


@router.delete(
    "/account",
    summary="Delete user account"
)
def delete_account(
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Soft delete the authenticated user's account.
    Sets is_active to False — data is retained.
    """
    user_service.delete_user(db, current_user_id)
    return {"message": "Account deactivated successfully"}
