"""
Conversation Service — manages the full AI interview conversation flow.

Responsibilities:
- Tracks conversation context across multiple questions
- Decides when to ask follow-up vs move to next question
- Maintains interview pacing and flow
- Generates natural conversational transitions between sections
- Handles candidate confusion or off-topic answers gracefully
"""
import logging
from typing import Optional
from sqlalchemy.orm import Session, joinedload

from app.models.interview import Interview, Question, Answer
from app.services.gemini_service import gemini_service
from app.services.answer_evaluator import answer_evaluator
from app.services.question_generator import question_generator
from app.core.exceptions import NotFoundError, BadRequestError

logger = logging.getLogger(__name__)


class ConversationService:
    """
    Manages the complete AI interview conversation.

    The interview flow:
    1. AI greets candidate and introduces itself
    2. For each question:
       a. AI asks the question
       b. Candidate speaks (Web Speech API → transcript)
       c. AI evaluates the answer
       d. If answer is too short/unclear → ask follow-up
       e. If answer is good → transition to next question
    3. AI wraps up and thanks the candidate
    """

    def get_next_question(
        self,
        db: Session,
        interview_id: int,
        user_id: int
    ) -> dict:
        """
        Get the next unanswered question in the interview.

        Returns:
            dict with question details and conversation context
            or end signal if all questions answered
        """
        interview = db.query(Interview).options(
            joinedload(Interview.questions),
            joinedload(Interview.job)
        ).filter(
            Interview.id == interview_id,
            Interview.user_id == user_id
        ).first()

        if not interview:
            raise NotFoundError("Interview not found")

        if interview.status == "completed":
            raise BadRequestError("Interview is already completed")

        # Get answered question IDs
        answered_ids = db.query(Answer.question_id).filter(
            Answer.user_id == user_id
        ).join(Question).filter(
            Question.interview_id == interview_id
        ).all()
        answered_ids = {r[0] for r in answered_ids}

        # Find next unanswered question
        questions = sorted(
            interview.questions,
            key=lambda q: q.question_order
        )

        next_question = None
        for q in questions:
            if q.id not in answered_ids:
                next_question = q
                break

        total = len(questions)
        answered_count = len(answered_ids)

        if not next_question:
            return {
                "interview_complete": True,
                "message": self._get_wrap_up_message(
                    interview.job.title if interview.job else "this role"
                ),
                "total_questions": total,
                "answered_questions": answered_count
            }

        # Generate AI transition message
        transition = self._get_transition_message(
            question_order=next_question.question_order,
            total_questions=total,
            answered_count=answered_count,
            job_title=(
                interview.job.title if interview.job else "this role"
            ),
            question_category=next_question.category
        )

        return {
            "interview_complete": False,
            "question": {
                "id": next_question.id,
                "question_text": next_question.question_text,
                "category": next_question.category,
                "difficulty": next_question.difficulty,
                "question_order": next_question.question_order,
                "expected_duration_seconds": (
                    next_question.expected_duration_seconds
                )
            },
            "transition_message": transition,
            "progress": {
                "current": answered_count + 1,
                "total": total,
                "percentage": int((answered_count / total) * 100)
            }
        }

    def process_answer(
        self,
        db: Session,
        interview_id: int,
        user_id: int,
        question_id: int,
        answer_text: str,
        duration_seconds: Optional[int] = None
    ) -> dict:
        """
        Process a candidate's spoken answer.

        Evaluates the answer, saves it, and determines whether to:
        - Ask a follow-up question (if answer was unclear/too short)
        - Move to the next question (if answer was sufficient)
        - Wrap up the interview (if all questions answered)

        Returns evaluation result + optional follow-up question.
        """
        # Verify interview and question exist
        interview = db.query(Interview).options(
            joinedload(Interview.job)
        ).filter(
            Interview.id == interview_id,
            Interview.user_id == user_id
        ).first()

        if not interview:
            raise NotFoundError("Interview not found")

        if interview.status == "completed":
            raise BadRequestError(
                "Cannot submit answer to completed interview"
            )

        question = db.query(Question).filter(
            Question.id == question_id,
            Question.interview_id == interview_id
        ).first()

        if not question:
            raise NotFoundError("Question not found in this interview")

        # Evaluate the answer
        job_title = interview.job.title if interview.job else "this role"
        required_skills = (
            interview.job.required_skills
            if interview.job else []
        ) or []

        evaluation = answer_evaluator.evaluate(
            question_text=question.question_text,
            answer_text=answer_text,
            job_title=job_title,
            required_skills=required_skills,
        )

        # Save the answer
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

        # Decide: follow-up or next question?
        follow_up = None
        needs_follow_up = self._needs_follow_up(
            evaluation, answer_text
        )

        if needs_follow_up:
            follow_up = question_generator.generate_follow_up(
                original_question=question.question_text,
                candidate_answer=answer_text,
                job_title=job_title
            )

        # Build response message
        response_message = self._build_response_message(
            evaluation=evaluation,
            has_follow_up=follow_up is not None
        )

        return {
            "answer_id": answer.id,
            "score": evaluation["score"],
            "feedback": evaluation["feedback"],
            "strengths": evaluation.get("strengths", []),
            "improvements": evaluation.get("improvements", []),
            "evaluation_method": evaluation.get(
                "evaluation_method", "nlp_only"
            ),
            "response_message": response_message,
            "follow_up_question": follow_up,
            "needs_follow_up": follow_up is not None
        }

    def get_interview_greeting(
        self,
        job_title: str,
        candidate_name: str,
        total_questions: int
    ) -> str:
        """
        Generate a personalized greeting for the start of the interview.
        Uses Gemini if available, falls back to template.
        """
        if gemini_service.is_available():
            try:
                prompt = f"""
You are an AI interviewer starting a job interview.

Generate a warm, professional, and concise greeting for:
- Candidate name: {candidate_name}
- Role: {job_title}
- Number of questions: {total_questions}

The greeting should:
1. Welcome the candidate by first name
2. Briefly explain the interview format
3. Mention they'll be speaking their answers
4. Be encouraging and set a comfortable tone
5. Be 3-4 sentences maximum

Return ONLY the greeting text, nothing else.
"""
                return gemini_service.generate_text(
                    prompt, temperature=0.6, max_tokens=200
                )
            except Exception as e:
                logger.warning(f"Greeting generation failed: {e}")

        # Fallback template
        first_name = candidate_name.split()[0] if candidate_name else "there"
        return (
            f"Hi {first_name}, welcome to your interview for the "
            f"{job_title} position. I'll be asking you {total_questions} "
            f"questions today. Please speak your answers clearly and take "
            f"your time. Let's get started!"
        )

    def generate_section_intro(
        self,
        section_name: str,
        job_title: str
    ) -> str:
        """
        Generate a smooth transition when moving to a new section.
        E.g., "Now let's move to the technical section..."
        """
        transitions = {
            "behavioral": (
                "Great. Now I'd like to learn more about your "
                "background and work style."
            ),
            "technical": (
                "Let's move on to the technical section. "
                "I'll ask you about your technical experience."
            ),
            "general": (
                "A few more general questions about your goals "
                "and how you stay current in your field."
            )
        }
        return transitions.get(
            section_name.lower(),
            "Let's continue to the next section."
        )

    def _needs_follow_up(
        self,
        evaluation: dict,
        answer_text: str
    ) -> bool:
        """
        Decide if the candidate's answer needs a follow-up.

        Follow-up triggered if:
        - Score is below 50 (poor answer)
        - Answer is very short (under 30 words)
        - Answer seems off-topic (score under 40)
        """
        word_count = len(answer_text.strip().split())
        score = evaluation.get("score", 0)

        if word_count < 20:
            return True
        if score < 40:
            return True
        return False

    def _get_transition_message(
        self,
        question_order: int,
        total_questions: int,
        answered_count: int,
        job_title: str,
        question_category: str
    ) -> str:
        """Generate a natural transition message before each question."""
        if question_order == 1:
            return (
                "Let's begin. Take your time with each answer "
                "and speak clearly."
            )
        elif answered_count == total_questions - 1:
            return "This is the final question."
        elif question_category == "technical":
            return "Now let's move to the technical questions."
        elif question_category == "behavioral":
            return "I'd like to understand your work style better."
        else:
            return "Moving on to the next question."

    def _get_wrap_up_message(self, job_title: str) -> str:
        """Generate a closing message when all questions are answered."""
        return (
            f"Thank you for completing the interview for the "
            f"{job_title} position. You've answered all the questions. "
            f"Please click 'End Interview' to see your results."
        )

    def _build_response_message(
        self,
        evaluation: dict,
        has_follow_up: bool
    ) -> str:
        """Build the AI's response message after receiving an answer."""
        score = evaluation.get("score", 0)

        if has_follow_up:
            return "I'd like to explore that a bit further."
        elif score >= 75:
            return "Thank you, that's a strong answer."
        elif score >= 55:
            return "Thank you for that answer."
        else:
            return "Thank you. Let's continue."


# Singleton instance
conversation_service = ConversationService()
