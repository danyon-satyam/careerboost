from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone
from app.services.answer_evaluator import answer_evaluator
from app.services.question_generator import question_generator

from app.models.interview import Interview, Question, Answer
from app.models.job import Job
from app.core.exceptions import NotFoundError, BadRequestError


# Default question bank — Week 2 replaces this with Gemini AI
DEFAULT_QUESTIONS = [
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
            "Describe a challenging problem you solved. "
            "What was your approach and what was the outcome?"
        ),
        "category": "behavioral",
        "difficulty": 2,
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
            "Where do you see yourself professionally in the next "
            "3 years, and how does this role fit into that plan?"
        ),
        "category": "behavioral",
        "difficulty": 1,
        "question_order": 5,
        "expected_duration_seconds": 90,
    },
]


class InterviewService:
    """Handles all DB operations and logic for Interviews."""

    def start_interview(
        self,
        db: Session,
        user_id: int,
        job_id: int
    ) -> Interview:
        """
        Start a new interview session for a user applying to a job.
        Creates the interview record and generates initial questions.
        Week 2: questions will be AI-generated based on resume + JD.
        """
        # Verify job exists
        job = db.query(Job).filter(
            Job.id == job_id,
            Job.is_active.is_(True)
        ).first()
        if not job:
            raise NotFoundError("Job not found")

        # Create interview record
        interview = Interview(
            user_id=user_id,
            job_id=job_id,
            status="in-progress",
            start_time=datetime.now(timezone.utc)
        )
        db.add(interview)
        db.flush()  # Get interview.id without committing

        # Generate AI questions based on job + candidate profile
        user = db.query(
            __import__(
                'app.models.user', fromlist=['User']
            ).User
        ).filter_by(id=user_id).first()

        candidate_skills = user.skills if user else []
        candidate_experience = user.experience_years if user else 0.0

        questions_data = question_generator.generate_questions(
            job_title=job.title,
            job_description=job.description,
            required_skills=job.required_skills or [],
            candidate_experience=candidate_experience,
            candidate_skills=candidate_skills,
            num_questions=5
        )

        for q_data in questions_data:
            question = Question(
                interview_id=interview.id,
                **q_data
            )
            db.add(question)

        db.commit()
        db.refresh(interview)
        return interview

    def get_by_id(
        self,
        db: Session,
        interview_id: int,
        user_id: Optional[int] = None
    ) -> Interview:
        """
        Fetch interview by ID.
        If user_id provided, verifies ownership.
        Raises NotFoundError if not found.
        """
        from sqlalchemy.orm import joinedload
        query = db.query(Interview).options(
            joinedload(Interview.job)
        ).filter(Interview.id == interview_id)
        if user_id:
            query = query.filter(Interview.user_id == user_id)

        interview = query.first()
        if not interview:
            raise NotFoundError("Interview not found")
        return interview

    def get_user_interviews(
        self,
        db: Session,
        user_id: int
    ) -> List[Interview]:
        """Get all interviews for a specific user."""
        return db.query(Interview).filter(
            Interview.user_id == user_id
        ).order_by(Interview.created_at.desc()).all()

    def submit_answer(
        self,
        db: Session,
        interview_id: int,
        user_id: int,
        question_id: int,
        answer_text: str,
        duration_seconds: Optional[int] = None
    ) -> Answer:
        """
        Submit a spoken answer for a question.
        Performs basic scoring — Week 2 replaces with
        Gemini + spaCy evaluation pipeline.
        """
        # Verify interview exists and belongs to user
        interview = self.get_by_id(db, interview_id, user_id)

        if interview.status != "in-progress":
            raise BadRequestError(
                "Cannot submit answer to a completed interview"
            )

        # Verify question belongs to this interview
        question = db.query(Question).filter(
            Question.id == question_id,
            Question.interview_id == interview_id
        ).first()
        if not question:
            raise NotFoundError("Question not found in this interview")

        # AI evaluation pipeline: spaCy → DuckDuckGo → Gemini
        evaluation = answer_evaluator.evaluate(
            question_text=question.question_text,
            answer_text=answer_text,
            job_title=interview.job.title,
            required_skills=interview.job.required_skills or [],
        )

        answer = Answer(
            question_id=question_id,
            user_id=user_id,
            answer_text=answer_text,
            duration_seconds=duration_seconds,
            score=evaluation["score"],
            feedback=evaluation["feedback"]
        )
        db.add(answer)
        db.commit()
        db.refresh(answer)
        return answer

    def end_interview(
        self,
        db: Session,
        interview_id: int,
        user_id: int
    ) -> Interview:
        """
        End an interview session and calculate final scores.
        Week 2: scores will be AI-calculated.
        """
        interview = self.get_by_id(db, interview_id, user_id)

        if interview.status == "completed":
            raise BadRequestError("Interview already completed")

        # Calculate scores from submitted answers
        answers = db.query(Answer).join(Question).filter(
            Question.interview_id == interview_id
        ).all()

        if answers:
            scores = [a.score for a in answers if a.score is not None]
            overall = int(sum(scores) / len(scores)) if scores else 50
        else:
            overall = 0

        now = datetime.now(timezone.utc)

        interview.status = "completed"
        interview.end_time = now
        interview.overall_score = overall
        interview.technical_score = overall
        interview.communication_score = overall
        interview.feedback_text = self._generate_feedback(overall)

        if interview.start_time:
            # Make start_time timezone-aware if it isn't already
            start = interview.start_time
            if start.tzinfo is None:
                start = start.replace(tzinfo=timezone.utc)
            delta = now - start
            interview.duration_seconds = int(delta.total_seconds())

        db.commit()
        db.refresh(interview)
        return interview

    def get_results(
        self,
        db: Session,
        interview_id: int,
        user_id: int
    ) -> dict:
        """Get interview results with scores and feedback."""
        interview = self.get_by_id(db, interview_id, user_id)

        total_questions = db.query(Question).filter(
            Question.interview_id == interview_id
        ).count()

        answered_questions = db.query(Answer).join(Question).filter(
            Question.interview_id == interview_id,
            Answer.user_id == user_id
        ).count()

        return {
            "id": interview.id,
            "status": interview.status,
            "overall_score": interview.overall_score,
            "communication_score": interview.communication_score,
            "technical_score": interview.technical_score,
            "feedback_text": interview.feedback_text,
            "total_questions": total_questions,
            "answered_questions": answered_questions,
        }

    def _basic_evaluate(self, answer_text: str) -> tuple:
        """
        Basic answer evaluation placeholder.
        Week 2: replaced with Gemini + spaCy pipeline.
        Scoring logic:
        - Very short answer (<20 words): 30-40
        - Short answer (20-50 words): 50-65
        - Good answer (50-100 words): 65-80
        - Detailed answer (100+ words): 75-90
        """
        word_count = len(answer_text.strip().split())

        if word_count < 20:
            score = 35
            feedback = (
                "Your answer was too brief. Try to elaborate more "
                "with specific examples and details."
            )
        elif word_count < 50:
            score = 58
            feedback = (
                "Good start, but your answer could be more detailed. "
                "Add specific examples from your experience."
            )
        elif word_count < 100:
            score = 72
            feedback = (
                "Good answer with reasonable detail. "
                "Consider adding measurable outcomes to strengthen it."
            )
        else:
            score = 82
            feedback = (
                "Detailed and well-structured answer. "
                "Good use of specific examples."
            )

        return score, feedback

    def _generate_feedback(self, overall_score: int) -> str:
        """Generate overall interview feedback based on score."""
        if overall_score >= 80:
            return (
                "Excellent performance! You demonstrated strong "
                "communication skills and technical knowledge. "
                "You are a strong candidate for this role."
            )
        elif overall_score >= 65:
            return (
                "Good performance overall. You showed solid understanding "
                "of the key areas. Consider providing more specific "
                "examples in your answers."
            )
        elif overall_score >= 50:
            return (
                "Moderate performance. You covered the basics but could "
                "strengthen your answers with more detail and "
                "specific examples from your experience."
            )
        else:
            return (
                "There is room for improvement. Focus on structuring "
                "your answers clearly and providing specific examples "
                "from your past experience."
            )


# Singleton instance
interview_service = InterviewService()
