"""
Question Generator Service — generates adaptive interview questions
using Gemini AI based on the job description and candidate profile.

Falls back to default questions if Gemini is unavailable.
"""
import logging
from typing import Optional

from app.services.gemini_service import gemini_service

logger = logging.getLogger(__name__)

# Fallback question bank when Gemini is unavailable
FALLBACK_QUESTIONS = [
    {
        "question_text": (
            "Tell me about yourself and your relevant experience "
            "for this role."
        ),
        "category": "behavioral",
        "difficulty": 1,
        "question_order": 1,
        "expected_duration_seconds": 120,
    },
    {
        "question_text": (
            "What are your strongest technical skills and how have "
            "you applied them in past projects?"
        ),
        "category": "technical",
        "difficulty": 2,
        "question_order": 2,
        "expected_duration_seconds": 120,
    },
    {
        "question_text": (
            "Describe a challenging technical problem you solved. "
            "What was your approach and the outcome?"
        ),
        "category": "technical",
        "difficulty": 3,
        "question_order": 3,
        "expected_duration_seconds": 150,
    },
    {
        "question_text": (
            "How do you stay updated with the latest technologies "
            "in your field?"
        ),
        "category": "general",
        "difficulty": 1,
        "question_order": 4,
        "expected_duration_seconds": 90,
    },
    {
        "question_text": (
            "Where do you see yourself professionally in 3 years "
            "and how does this role fit into that plan?"
        ),
        "category": "behavioral",
        "difficulty": 1,
        "question_order": 5,
        "expected_duration_seconds": 90,
    },
]


class QuestionGenerator:
    """
    Generates adaptive interview questions using Gemini AI.
    Falls back to default questions if AI is unavailable.
    """

    def generate_questions(
        self,
        job_title: str,
        job_description: str,
        required_skills: list,
        candidate_experience: float = 0.0,
        candidate_skills: Optional[list] = None,
        num_questions: int = 5
    ) -> list:
        """
        Generate interview questions for a specific job and candidate.

        Returns list of question dicts ready to be saved as
        Question model instances.
        """
        # Try AI generation first
        if gemini_service.is_available():
            try:
                questions = gemini_service.generate_interview_questions(
                    job_title=job_title,
                    job_description=job_description,
                    required_skills=required_skills,
                    candidate_experience=candidate_experience,
                    candidate_skills=candidate_skills,
                    num_questions=num_questions
                )
                logger.info(
                    f"Generated {len(questions)} AI questions "
                    f"for {job_title}"
                )
                return questions
            except Exception as e:
                logger.warning(
                    f"AI question generation failed, "
                    f"using fallback: {e}"
                )

        # Fallback: return default questions
        logger.info(
            "Using fallback questions "
            "(Gemini unavailable or failed)"
        )
        return FALLBACK_QUESTIONS[:num_questions]

    def generate_follow_up(
        self,
        original_question: str,
        candidate_answer: str,
        job_title: str
    ) -> Optional[str]:
        """
        Generate a conversational follow-up question.
        Returns None if AI is unavailable.
        """
        if not gemini_service.is_available():
            return None

        try:
            return gemini_service.generate_follow_up_question(
                original_question=original_question,
                candidate_answer=candidate_answer,
                job_title=job_title
            )
        except Exception as e:
            logger.warning(f"Follow-up generation failed: {e}")
            return None


# Singleton instance
question_generator = QuestionGenerator()
