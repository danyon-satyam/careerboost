from fastapi import Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.security import get_current_user_id
from app.models.user import User
from app.services.user_service import user_service


def get_current_user(
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> User:
    """
    FastAPI dependency that returns the full User object.
    Use this when you need the user model, not just the ID.
    """
    return user_service.get_by_id(db, current_user_id)


class PaginationParams:
    """Reusable pagination dependency for list endpoints."""
    def __init__(
        self,
        page: int = Query(default=1, ge=1, description="Page number"),
        page_size: int = Query(
            default=20, ge=1, le=100, description="Items per page"
        )
    ):
        self.page = page
        self.page_size = page_size
        self.offset = (page - 1) * page_size
