from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.security import get_current_user_id
from app.schemas.user import UserResponse, UserUpdate
from app.services.user_service import user_service
from app.services.resume_parser import resume_parser

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
    """Get the authenticated user's profile."""
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


@router.post(
    "/resume",
    response_model=UserResponse,
    summary="Upload and parse resume PDF"
)
async def upload_resume(
    file: UploadFile = File(...),
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Upload a PDF resume — auto-extracts skills and experience.

    - Accepts PDF files only
    - Extracts skills, experience years, education
    - Automatically updates the user's profile with parsed data
    - Returns updated user profile
    """
    if not file.filename.endswith(".pdf"):
        from app.core.exceptions import BadRequestError
        raise BadRequestError("Only PDF files are supported")

    file_bytes = await file.read()
    parsed = resume_parser.parse_pdf(file_bytes)

    # Build update data from parsed resume
    update_data = {
        "resume_text": file_bytes.decode("utf-8", errors="ignore"),
    }

    if parsed["parse_success"]:
        if parsed["skills"]:
            update_data["skills"] = parsed["skills"]
        if parsed["experience_years"] > 0:
            update_data["experience_years"] = parsed["experience_years"]
        if parsed["summary"]:
            update_data["profile_summary"] = parsed["summary"]

    return user_service.update_user(
        db, current_user_id, update_data
    )


@router.get(
    "/stats",
    summary="Get user statistics"
)
def get_user_stats(
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get interview and typing statistics for the authenticated user."""
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
    """Soft delete the authenticated user's account."""
    user_service.delete_user(db, current_user_id)
    return {"message": "Account deactivated successfully"}
