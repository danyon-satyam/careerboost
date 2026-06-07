from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional, List

from app.models.job import Job
from app.core.exceptions import NotFoundError


class JobService:
    """Handles all DB operations for Jobs."""

    def create_job(self, db: Session, job_data: dict) -> Job:
        """Create a new job posting."""
        job = Job(**job_data)
        db.add(job)
        db.commit()
        db.refresh(job)
        return job

    def get_by_id(self, db: Session, job_id: int) -> Job:
        """Fetch job by ID. Raises NotFoundError if not found."""
        job = db.query(Job).filter(
            Job.id == job_id,
            Job.is_active == True
        ).first()
        if not job:
            raise NotFoundError("Job not found")
        return job

    def get_all(
        self,
        db: Session,
        page: int = 1,
        page_size: int = 20,
        location: Optional[str] = None,
        job_type: Optional[str] = None,
        min_salary: Optional[float] = None,
        max_salary: Optional[float] = None,
    ) -> dict:
        """
        Get paginated job listings with optional filters.
        Returns jobs + total count + pagination info.
        """
        query = db.query(Job).filter(Job.is_active == True)

        if location:
            query = query.filter(
                Job.location.ilike(f"%{location}%")
            )
        if job_type:
            query = query.filter(Job.job_type == job_type)
        if min_salary is not None:
            query = query.filter(Job.salary_min >= min_salary)
        if max_salary is not None:
            query = query.filter(Job.salary_max <= max_salary)

        total = query.count()
        offset = (page - 1) * page_size
        jobs = query.order_by(
            Job.posted_date.desc()
        ).offset(offset).limit(page_size).all()

        return {
            "jobs": jobs,
            "total": total,
            "page": page,
            "page_size": page_size
        }

    def search(
        self,
        db: Session,
        query_str: str,
        page: int = 1,
        page_size: int = 20
    ) -> dict:
        """
        Search jobs by keyword across title, company,
        description, and location.
        """
        search_term = f"%{query_str.strip()}%"

        query = db.query(Job).filter(
            Job.is_active == True,
            or_(
                Job.title.ilike(search_term),
                Job.company.ilike(search_term),
                Job.description.ilike(search_term),
                Job.location.ilike(search_term),
            )
        )

        total = query.count()
        offset = (page - 1) * page_size
        jobs = query.order_by(
            Job.posted_date.desc()
        ).offset(offset).limit(page_size).all()

        return {
            "jobs": jobs,
            "total": total,
            "query": query_str
        }

    def get_similar(
        self,
        db: Session,
        job_id: int,
        limit: int = 5
    ) -> List[Job]:
        """
        Get similar jobs based on location and job_type.
        Week 3 will enhance this with ML-based matching.
        """
        job = self.get_by_id(db, job_id)

        similar = db.query(Job).filter(
            Job.id != job_id,
            Job.is_active == True,
            or_(
                Job.location == job.location,
                Job.job_type == job.job_type,
            )
        ).limit(limit).all()

        return similar

    def deactivate_job(self, db: Session, job_id: int) -> bool:
        """Soft delete — sets is_active to False."""
        job = self.get_by_id(db, job_id)
        job.is_active = False
        db.commit()
        return True


# Singleton instance
job_service = JobService()
