"""
Resume Parser Service — extracts structured information from PDF resumes.

Uses PyPDF2 for text extraction and spaCy NLP for entity recognition.
Falls back to regex patterns if spaCy is unavailable.
Zero API calls — completely free and offline.
"""
import re
import logging
from typing import Optional
from io import BytesIO

from app.services.nlp_service import nlp_service

logger = logging.getLogger(__name__)

# Comprehensive tech skills list for matching
KNOWN_SKILLS = [
    # Languages
    "python", "javascript", "typescript", "java", "c++", "c#",
    "go", "rust", "ruby", "php", "swift", "kotlin", "scala",
    "r", "matlab", "perl",
    # Web frameworks
    "fastapi", "django", "flask", "express", "nestjs", "spring",
    "rails", "laravel", "react", "vue", "angular", "nextjs",
    "nuxtjs", "svelte",
    # Databases
    "postgresql", "mysql", "mongodb", "redis", "sqlite",
    "cassandra", "elasticsearch", "dynamodb", "firebase",
    "oracle", "sql server", "mariadb",
    # Cloud & DevOps
    "aws", "gcp", "azure", "docker", "kubernetes", "terraform",
    "ansible", "jenkins", "github actions", "gitlab ci",
    "circleci", "cloud run", "lambda", "ec2", "s3",
    # ML/AI
    "tensorflow", "pytorch", "scikit-learn", "keras",
    "hugging face", "spacy", "nltk", "pandas", "numpy",
    "matplotlib", "seaborn", "jupyter",
    # Tools & Others
    "git", "linux", "bash", "rest api", "graphql",
    "microservices", "agile", "scrum", "ci/cd", "tdd",
    "html", "css", "tailwind", "bootstrap", "figma",
]

# Degree keywords
DEGREE_KEYWORDS = [
    "b.tech", "btech", "b.e", "be ", "bachelor",
    "m.tech", "mtech", "m.e", "me ", "master",
    "mba", "phd", "ph.d", "bsc", "msc",
    "b.sc", "m.sc", "diploma",
]

# Experience section keywords
EXPERIENCE_KEYWORDS = [
    "experience", "work experience", "employment",
    "professional experience", "career", "work history",
]


class ResumeParser:
    """
    Parses PDF resumes to extract structured candidate information.

    Extracted data:
    - skills: list of technical skills found
    - experience_years: estimated total years of experience
    - education: highest degree found
    - summary: brief professional summary
    - contact: email if found
    """

    def parse_pdf(self, file_bytes: bytes) -> dict:
        """
        Parse a PDF resume from bytes.

        Args:
            file_bytes: Raw PDF file bytes

        Returns:
            dict with skills, experience_years, education, summary
        """
        try:
            text = self._extract_text(file_bytes)
            if not text or len(text.strip()) < 50:
                return self._empty_result("Could not extract text from PDF")

            return self._parse_text(text)

        except Exception as e:
            logger.error(f"Resume parsing failed: {e}")
            return self._empty_result(f"Parsing error: {str(e)}")

    def parse_text(self, resume_text: str) -> dict:
        """
        Parse resume from plain text (already extracted).

        Args:
            resume_text: Resume content as string

        Returns:
            dict with extracted information
        """
        if not resume_text or len(resume_text.strip()) < 50:
            return self._empty_result("Resume text too short")

        return self._parse_text(resume_text)

    def _extract_text(self, file_bytes: bytes) -> str:
        """Extract raw text from PDF bytes using PyPDF2."""
        try:
            import PyPDF2
            reader = PyPDF2.PdfReader(BytesIO(file_bytes))
            text_parts = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
            return "\n".join(text_parts)
        except Exception as e:
            logger.warning(f"PyPDF2 extraction failed: {e}")
            return ""

    def _parse_text(self, text: str) -> dict:
        """Core parsing logic — extracts all fields from text."""
        text_lower = text.lower()

        skills = self._extract_skills(text_lower)
        experience_years = self._extract_experience_years(text)
        education = self._extract_education(text_lower)
        email = self._extract_email(text)
        summary = self._generate_summary(
            text, skills, experience_years
        )

        return {
            "skills": skills,
            "experience_years": experience_years,
            "education": education,
            "email": email,
            "summary": summary,
            "raw_text_length": len(text),
            "parse_success": True
        }

    def _extract_skills(self, text_lower: str) -> list:
        """
        Extract technical skills from resume text.
        Combines known skills list + spaCy NLP extraction.
        """
        found_skills = []

        # Method 1: Match against known skills list
        for skill in KNOWN_SKILLS:
            if skill in text_lower:
                found_skills.append(skill)

        # Method 2: Use spaCy to find additional technical terms
        nlp_skills = nlp_service.extract_skills_from_text(text_lower)
        for skill in nlp_skills:
            if skill not in found_skills:
                found_skills.append(skill)

        # Deduplicate and sort
        return sorted(list(set(found_skills)))

    def _extract_experience_years(self, text: str) -> float:
        """
        Estimate total years of experience from resume text.

        Strategies:
        1. Look for explicit "X years of experience" patterns
        2. Count date ranges in work experience sections
        3. Default to 0 if nothing found
        """
        # Strategy 1: Direct mention pattern
        patterns = [
            r"(\d+)\+?\s*years?\s*(?:of\s*)?experience",
            r"experience\s*(?:of\s*)?(\d+)\+?\s*years?",
            r"(\d+)\+?\s*yrs?\s*(?:of\s*)?experience",
        ]

        for pattern in patterns:
            matches = re.findall(
                pattern, text.lower()
            )
            if matches:
                try:
                    years = max(int(m) for m in matches)
                    return float(min(years, 50))
                except ValueError:
                    continue

        # Strategy 2: Count date ranges (e.g., 2020-2023)
        date_pattern = r"\b(20\d{2})\s*[-–]\s*(20\d{2}|present|current)\b"
        date_ranges = re.findall(
            date_pattern, text.lower()
        )

        if date_ranges:
            total_years = 0
            current_year = 2025
            for start, end in date_ranges:
                try:
                    start_yr = int(start)
                    end_yr = (
                        current_year
                        if end in ("present", "current")
                        else int(end)
                    )
                    if 2000 <= start_yr <= current_year:
                        total_years += max(0, end_yr - start_yr)
                except ValueError:
                    continue
            if total_years > 0:
                return float(min(total_years, 50))

        # Strategy 3: Count job entries as rough estimate
        job_count = len(re.findall(
            r"\b(?:engineer|developer|analyst|manager|intern)\b",
            text.lower()
        ))
        if job_count >= 3:
            return 2.0
        elif job_count >= 1:
            return 1.0

        return 0.0

    def _extract_education(self, text_lower: str) -> str:
        """Extract highest education level from resume."""
        # Priority order — check from highest to lowest
        if any(k in text_lower for k in ["phd", "ph.d"]):
            return "PhD"
        if any(k in text_lower for k in ["mtech", "m.tech", "master"]):
            return "Master's"
        if "mba" in text_lower:
            return "MBA"
        if any(k in text_lower for k in ["msc", "m.sc"]):
            return "MSc"
        if any(k in text_lower for k in [
            "btech", "b.tech", "bachelor", "b.e", "be "
        ]):
            return "Bachelor's"
        if any(k in text_lower for k in ["bsc", "b.sc"]):
            return "BSc"
        if "diploma" in text_lower:
            return "Diploma"
        return "Not specified"

    def _extract_email(self, text: str) -> Optional[str]:
        """Extract email address from resume text."""
        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        matches = re.findall(pattern, text)
        return matches[0] if matches else None

    def _generate_summary(
        self,
        text: str,
        skills: list,
        experience_years: float
    ) -> str:
        """Generate a brief summary of the candidate's profile."""
        skill_count = len(skills)
        top_skills = ", ".join(skills[:5]) if skills else "various technologies"

        if experience_years >= 5:
            level = "Senior"
        elif experience_years >= 2:
            level = "Mid-level"
        elif experience_years >= 1:
            level = "Junior"
        else:
            level = "Entry-level"

        return (
            f"{level} professional with {experience_years:.1f} years "
            f"of experience. "
            f"Key skills: {top_skills}. "
            f"Total {skill_count} technical skills identified."
        )

    def _empty_result(self, reason: str) -> dict:
        """Return empty result structure when parsing fails."""
        return {
            "skills": [],
            "experience_years": 0.0,
            "education": "Not specified",
            "email": None,
            "summary": "",
            "raw_text_length": 0,
            "parse_success": False,
            "error": reason
        }


# Singleton instance
resume_parser = ResumeParser()
