"""
JD Parser Service — extracts structured data from raw job description
text using existing NLP infrastructure, creates a Job record, and
starts an interview in one atomic operation.
"""
import logging
import re
from typing import Optional
from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.user import User
from app.services.nlp_service import nlp_service
from app.services.interview_service import interview_service

logger = logging.getLogger(__name__)

# Common experience patterns
_EXP_PATTERNS = [
    r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s+)?(?:experience|exp)',
    r'(?:minimum|min|at least)\s+(\d+)\s*(?:years?|yrs?)',
    r'(\d+)\s*-\s*\d+\s*(?:years?|yrs?)\s*(?:of\s+)?(?:experience|exp)',
]

_DEFAULT_TITLE = "Software Engineer"
_DEFAULT_COMPANY = "Tech Company"


class JDParserService:
    """
    Parses freeform JD text into a structured Job + Interview.

    Pipeline:
    1. Extract role title (regex + heuristic)
    2. Extract company name (heuristic)
    3. Extract required skills (nlp_service)
    4. Extract experience years (regex)
    5. Create Job record in DB
    6. Call interview_service.start_interview
    7. Return combined result
    """

    def parse_and_start(
        self,
        db: Session,
        user: User,
        jd_text: str,
        title_override: Optional[str] = None,
        company_override: Optional[str] = None,
    ) -> dict:
        """
        Parse JD text and immediately start an interview.

        Returns a dict matching JDParseResponse schema.
        """
        title = title_override or self._extract_title(jd_text)
        company = company_override or self._extract_company(jd_text)
        skills = self._extract_skills(jd_text)
        experience = self._extract_experience(jd_text)
        description = jd_text[:1000]

        # Create an ephemeral Job record
        job = Job(
            title=title,
            company=company,
            description=description,
            required_skills=skills,
            required_experience=experience,
            location="Not specified",
            job_type="full-time",
            is_active=True,
        )
        db.add(job)
        db.commit()
        db.refresh(job)

        # Start the interview using existing service
        interview = interview_service.start_interview(
            db=db,
            user_id=user.id,
            job_id=job.id
        )

        # Build sections from question categories
        sections = list(set(
            q.category for q in interview.questions
            if q.category
        ))

        return {
            "interview_id": interview.id,
            "job_id": job.id,
            "title": title,
            "company": company,
            "extracted_skills": skills,
            "required_experience": experience,
            "questions": interview.questions,
            "total_questions": len(interview.questions),
            "sections": sections,
            "status": interview.status,
        }

    def _extract_title(self, text: str) -> str:
        """
        Extract job title from JD text.
        Looks for common patterns like 'Role: X', 'Position: X',
        or falls back to first noun phrase.
        """
        patterns = [
            r'(?:role|position|job title|title)[:\s]+([^\n,\.]{5,60})',
            r'(?:we are|we\'re) (?:looking|hiring) for (?:a|an) ([^\n,\.]{5,60})',
            r'(?:^|\n)([A-Z][a-z]+ (?:Engineer|Developer|Designer|Manager|Analyst|Scientist|Lead|Architect)[^\n]{0,30})',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()[:100]

        return _DEFAULT_TITLE

    def _extract_company(self, text: str) -> str:
        """
        Extract company name from JD text.
        Looks for 'at CompanyName', 'join CompanyName', etc.
        """
        patterns = [
            r'(?:at|join|about|company[:\s]+)([A-Z][A-Za-z0-9\s&\.]{2,40})(?:\s+is|\s+are|\s+,|\.|$)',
            r'(?:^|\n)(?:About\s+)([A-Z][A-Za-z0-9\s&\.]{2,40})\n',
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                candidate = match.group(1).strip()
                if len(candidate) > 2:
                    return candidate[:100]

        return _DEFAULT_COMPANY

    def _extract_skills(self, text: str) -> list:
        """
        Use nlp_service to extract skills from JD text.
        Falls back to keyword matching if spaCy unavailable.
        """
        try:
            return nlp_service.extract_skills_from_text(text)[:15]
        except Exception as e:
            logger.warning(
                f"NLP skill extraction failed, using keywords: {e}"
            )
            return self._keyword_skills(text)

    def _extract_experience(self, text: str) -> int:
        """Extract required years of experience from JD text."""
        for pattern in _EXP_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    years = int(match.group(1))
                    return min(years, 20)
                except (ValueError, IndexError):
                    continue
        return 2

    def _keyword_skills(self, text: str) -> list:
        """Keyword-based skill fallback."""
        KNOWN_SKILLS = [
            "python", "javascript", "typescript", "react", "node.js",
            "fastapi", "django", "flask", "postgresql", "mysql",
            "mongodb", "redis", "docker", "kubernetes", "aws", "gcp",
            "azure", "git", "sql", "graphql", "rest", "api", "java",
            "spring", "go", "rust", "c++", "machine learning", "ai",
        ]
        text_lower = text.lower()
        return [s for s in KNOWN_SKILLS if s in text_lower][:12]


jd_parser_service = JDParserService()
