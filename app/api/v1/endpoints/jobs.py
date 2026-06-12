from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.db.database import get_db
from app.core.security import get_current_user_id
from app.schemas.job import JobCreate, JobResponse, JobListResponse, JobSearchResponse
from app.services.job_service import job_service
from app.services.job_matcher import job_matcher_service
from app.services.user_service import user_service as _user_service

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get(
    "",
    response_model=JobListResponse,
    summary="List all jobs with pagination and filters"
)
def list_jobs(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    location: Optional[str] = Query(default=None),
    job_type: Optional[str] = Query(default=None),
    min_salary: Optional[float] = Query(default=None),
    max_salary: Optional[float] = Query(default=None),
    db: Session = Depends(get_db)
):
    """
    Get paginated list of active jobs.

    Filters available:
    - **location**: filter by city or region
    - **job_type**: full-time, part-time, remote, contract, internship
    - **min_salary**: minimum salary range
    - **max_salary**: maximum salary range
    """
    return job_service.get_all(
        db=db,
        page=page,
        page_size=page_size,
        location=location,
        job_type=job_type,
        min_salary=min_salary,
        max_salary=max_salary
    )


@router.get(
    "/search",
    response_model=JobSearchResponse,
    summary="Search jobs by keyword"
)
def search_jobs(
    q: str = Query(..., min_length=1, description="Search keyword"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Search jobs by keyword across title, company,
    description, and location.

    - **q**: search term (required)
    """
    return job_service.search(
        db=db,
        query_str=q,
        page=page,
        page_size=page_size
    )


@router.get(
    "/recommendations",
    summary="Get personalized job recommendations"
)
def get_recommendations(
    limit: int = Query(default=10, ge=1, le=50),
    min_score: int = Query(default=30, ge=0, le=100),
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Get AI-powered job recommendations based on your profile.

    Scoring uses:
    - Skill match (40%): how many required skills you have
    - Experience match (30%): your years vs required
    - Semantic similarity (30%): NLP profile matching

    Update your profile skills to improve recommendations.
    """
    user = _user_service.get_by_id(db, current_user_id)
    recommendations = job_matcher_service.get_recommendations(
        db=db,
        user=user,
        limit=limit,
        min_score=min_score
    )

    return {
        "recommendations": [
            {
                "job_id": r["job"].id,
                "title": r["job"].title,
                "company": r["job"].company,
                "location": r["job"].location,
                "job_type": r["job"].job_type,
                "match_score": r["match_score"],
                "matched_skills": r["matched_skills"],
                "missing_skills": r["missing_skills"],
                "recommendation": r["recommendation"]
            }
            for r in recommendations
        ],
        "total": len(recommendations),
        "user_skills_count": len(user.skills or [])
    }


@router.get(
    "/{job_id}",
    response_model=JobResponse,
    summary="Get job details by ID"
)
def get_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    """Get full details of a specific job by its ID."""
    return job_service.get_by_id(db, job_id)


@router.get(
    "/{job_id}/similar",
    response_model=list[JobResponse],
    summary="Get similar jobs"
)
def get_similar_jobs(
    job_id: int,
    db: Session = Depends(get_db)
):
    """
    Get jobs similar to this one based on location and type.
    ML-based similarity added in Week 3.
    """
    return job_service.get_similar(db, job_id)


@router.get(
    "/{job_id}/match-score",
    summary="Get match score for a specific job"
)
def get_job_match_score(
    job_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Get your personal match score for a specific job.
    Returns detailed breakdown of skill and experience match.
    """
    job = job_service.get_by_id(db, job_id)
    user = _user_service.get_by_id(db, current_user_id)
    return job_matcher_service.calculate_match_score(user, job)
    

@router.post(
    "",
    response_model=JobResponse,
    status_code=201,
    summary="Create a new job posting"
)
def create_job(
    payload: JobCreate,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Create a new job posting. Requires authentication.

    - **title**: job title
    - **company**: company name
    - **description**: full job description
    - **required_skills**: list of required skills
    - **required_experience**: years of experience needed
    - **job_type**: full-time, part-time, remote, contract, internship
    """
    return job_service.create_job(
        db=db,
        job_data=payload.model_dump()
    )


@router.delete(
    "/{job_id}",
    summary="Deactivate a job posting"
)
def deactivate_job(
    job_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Deactivate a job posting. Requires authentication.
    Job is soft-deleted — data is retained.
    """
    job_service.deactivate_job(db, job_id)
    return {"message": f"Job {job_id} deactivated successfully"}
