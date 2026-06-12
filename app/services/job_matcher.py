"""
Job Matcher Service — calculates match scores between candidates
and job postings using skill overlap and experience matching.

Uses sentence-transformers for semantic similarity when available,
falls back to keyword matching. Zero external API calls.
"""
import logging
from typing import Optional
from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.user import User
from app.services.nlp_service import nlp_service

logger = logging.getLogger(__name__)

# Try to import sentence-transformers for semantic matching
try:
    from sentence_transformers import SentenceTransformer, util
    _model = SentenceTransformer("all-MiniLM-L6-v2")
    SEMANTIC_AVAILABLE = True
    logger.info("Sentence transformer loaded for job matching")
except Exception:
    SEMANTIC_AVAILABLE = False
    logger.info(
        "Sentence transformer unavailable, using keyword matching"
    )


class JobMatcherService:
    """
    Calculates how well a candidate matches a job posting.

    Scoring components:
    - Skill match: % of required skills the candidate has (40%)
    - Experience match: years of experience vs required (30%)
    - Semantic similarity: NLP similarity of profiles (30%)
    """

    def calculate_match_score(
        self,
        user: User,
        job: Job
    ) -> dict:
        """
        Calculate comprehensive match score between user and job.

        Returns:
            dict with match_score (0-100), matched_skills,
            missing_skills, experience_match, recommendation
        """
        user_skills = [
            s.lower() for s in (user.skills or [])
        ]
        required_skills = [
            s.lower() for s in (job.required_skills or [])
        ]

        # Component 1: Skill match (40% weight)
        skill_result = self._calculate_skill_match(
            user_skills, required_skills
        )
        skill_score = skill_result["score"]

        # Component 2: Experience match (30% weight)
        exp_score = self._calculate_experience_match(
            user.experience_years or 0.0,
            job.required_experience or 0
        )

        # Component 3: Semantic similarity (30% weight)
        semantic_score = self._calculate_semantic_similarity(
            user, job
        )

        # Weighted final score
        final_score = int(
            (skill_score * 0.40) +
            (exp_score * 0.30) +
            (semantic_score * 0.30)
        )
        final_score = min(100, max(0, final_score))

        return {
            "match_score": final_score,
            "matched_skills": skill_result["matched"],
            "missing_skills": skill_result["missing"],
            "skill_score": skill_score,
            "experience_score": exp_score,
            "semantic_score": semantic_score,
            "experience_years_user": user.experience_years or 0.0,
            "experience_years_required": job.required_experience or 0,
            "recommendation": self._get_recommendation(final_score)
        }

    def get_recommendations(
        self,
        db: Session,
        user: User,
        limit: int = 10,
        min_score: int = 30
    ) -> list:
        """
        Get top job recommendations for a user.

        Scores all active jobs and returns top matches
        above the minimum score threshold.
        """
        jobs = db.query(Job).filter(
            Job.is_active.is_(True)
        ).all()

        scored_jobs = []
        for job in jobs:
            try:
                match = self.calculate_match_score(user, job)
                if match["match_score"] >= min_score:
                    scored_jobs.append({
                        "job": job,
                        "match_score": match["match_score"],
                        "matched_skills": match["matched_skills"],
                        "missing_skills": match["missing_skills"],
                        "recommendation": match["recommendation"]
                    })
            except Exception as e:
                logger.warning(
                    f"Match score failed for job {job.id}: {e}"
                )

        # Sort by score descending
        scored_jobs.sort(
            key=lambda x: x["match_score"], reverse=True
        )
        return scored_jobs[:limit]

    def _calculate_skill_match(
        self,
        user_skills: list,
        required_skills: list
    ) -> dict:
        """Calculate skill overlap between user and job."""
        if not required_skills:
            return {"score": 80, "matched": [], "missing": []}

        matched = [
            skill for skill in required_skills
            if skill in user_skills
        ]
        missing = [
            skill for skill in required_skills
            if skill not in user_skills
        ]

        coverage = len(matched) / len(required_skills)
        score = int(coverage * 100)

        return {
            "score": score,
            "matched": matched,
            "missing": missing
        }

    def _calculate_experience_match(
        self,
        user_years: float,
        required_years: int
    ) -> int:
        """
        Calculate experience match score.

        Rules:
        - Exact match or more: 100
        - Within 1 year short: 80
        - Within 2 years short: 60
        - Within 3 years short: 40
        - More than 3 years short: 20
        - No experience required: 100
        """
        if required_years <= 0:
            return 100

        gap = required_years - user_years

        if gap <= 0:
            return 100
        elif gap <= 1:
            return 80
        elif gap <= 2:
            return 60
        elif gap <= 3:
            return 40
        else:
            return 20

    def _calculate_semantic_similarity(
        self,
        user: User,
        job: Job
    ) -> int:
        """
        Calculate semantic similarity between candidate profile
        and job description using sentence-transformers.

        Falls back to keyword overlap if model unavailable.
        """
        # Build candidate profile text
        user_text_parts = []
        if user.profile_summary:
            user_text_parts.append(user.profile_summary)
        if user.skills:
            user_text_parts.append(" ".join(user.skills))
        if user.current_position:
            user_text_parts.append(user.current_position)
        if user.target_role:
            user_text_parts.append(user.target_role)

        user_text = " ".join(user_text_parts).strip()

        # Build job text
        job_text_parts = [job.title]
        if job.description:
            job_text_parts.append(job.description[:500])
        if job.required_skills:
            job_text_parts.append(" ".join(job.required_skills))

        job_text = " ".join(job_text_parts).strip()

        if not user_text or not job_text:
            return 50

        # Try semantic similarity with sentence-transformers
        if SEMANTIC_AVAILABLE:
            try:
                embeddings = _model.encode(
                    [user_text, job_text],
                    convert_to_tensor=True
                )
                similarity = util.cos_sim(
                    embeddings[0], embeddings[1]
                ).item()
                return int(max(0, min(100, similarity * 100)))
            except Exception as e:
                logger.warning(
                    f"Semantic similarity failed: {e}"
                )

        # Fallback: keyword overlap
        return self._keyword_overlap_score(user_text, job_text)

    def _keyword_overlap_score(
        self,
        text1: str,
        text2: str
    ) -> int:
        """Simple keyword overlap as fallback similarity."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        if not words1 or not words2:
            return 50
        overlap = len(words1 & words2)
        union = len(words1 | words2)
        jaccard = overlap / union if union > 0 else 0
        return int(jaccard * 100)

    def _get_recommendation(self, score: int) -> str:
        """Get hiring recommendation label based on score."""
        if score >= 80:
            return "Strong Match"
        elif score >= 60:
            return "Good Match"
        elif score >= 40:
            return "Partial Match"
        else:
            return "Weak Match"


# Singleton instance
job_matcher_service = JobMatcherService()
