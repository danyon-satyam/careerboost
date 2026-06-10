"""
Answer Evaluator Service — the AI evaluation pipeline.

Pipeline:
1. spaCy NLP → local quality analysis (free, instant, offline)
2. DuckDuckGo → fetch real-time technical context (free, no key)
3. Gemini AI → semantic evaluation with web context (free tier)

Falls back gracefully if Gemini is unavailable.
"""
import logging
from typing import Optional

from app.services.nlp_service import nlp_service
from app.services.web_search_service import web_search_service
from app.services.gemini_service import gemini_service

logger = logging.getLogger(__name__)


class AnswerEvaluator:
    """
    Evaluates candidate's spoken interview answers using a
    three-stage AI pipeline: spaCy → DuckDuckGo → Gemini.
    """

    def evaluate(
        self,
        question_text: str,
        answer_text: str,
        job_title: str,
        required_skills: list,
        use_ai: bool = True
    ) -> dict:
        """
        Full evaluation pipeline for a spoken answer.

        Args:
            question_text: The interview question asked
            answer_text: Candidate's spoken answer transcript
            job_title: Role being interviewed for
            required_skills: Skills required for the job
            use_ai: If True, uses Gemini. If False, uses NLP only.

        Returns:
            dict with score (0-100), feedback, strengths, improvements
        """
        # Stage 1: Always run local NLP analysis (free, instant)
        nlp_result = nlp_service.get_answer_quality_score(answer_text)
        skill_coverage = nlp_service.calculate_skill_coverage(
            answer_text, required_skills
        )

        # If answer is too short, return immediately without AI call
        if nlp_result["word_count"] < 10:
            return {
                "score": 20,
                "feedback": (
                    "Your answer was too brief. Please speak in complete "
                    "sentences and provide specific details and examples."
                ),
                "strengths": [],
                "improvements": [
                    "Provide a more detailed answer",
                    "Use specific examples from your experience"
                ],
                "nlp_analysis": nlp_result,
                "evaluation_method": "nlp_only"
            }

        # If AI is disabled or Gemini not configured, use NLP only
        if not use_ai or not gemini_service.is_available():
            return self._nlp_only_evaluation(
                nlp_result, skill_coverage, required_skills
            )

        # Stage 2: Get web search context for technical accuracy
        web_context = self._get_web_context(
            question_text, job_title, required_skills
        )

        # Stage 3: Gemini AI evaluation with full context
        try:
            ai_result = gemini_service.evaluate_answer(
                question_text=question_text,
                answer_text=answer_text,
                job_title=job_title,
                required_skills=required_skills,
                web_search_context=web_context
            )

            # Blend AI score with NLP quality score
            blended_score = self._blend_scores(
                ai_score=ai_result["score"],
                nlp_score=nlp_result["score"],
                skill_coverage=skill_coverage
            )

            return {
                "score": blended_score,
                "feedback": ai_result["feedback"],
                "strengths": ai_result.get("strengths", []),
                "improvements": ai_result.get("improvements", []),
                "nlp_analysis": nlp_result,
                "evaluation_method": "ai_pipeline"
            }

        except Exception as e:
            # Gemini failed — fall back to NLP gracefully
            logger.warning(f"Gemini evaluation failed, using NLP: {e}")
            return self._nlp_only_evaluation(
                nlp_result, skill_coverage, required_skills
            )

    def _get_web_context(
        self,
        question_text: str,
        job_title: str,
        required_skills: list
    ) -> Optional[str]:
        """
        Fetch relevant technical context from the web.
        Uses the most relevant skill mentioned in the question.
        """
        try:
            # Find the most relevant skill to search for
            question_lower = question_text.lower()
            relevant_skill = None

            for skill in required_skills:
                if skill.lower() in question_lower:
                    relevant_skill = skill
                    break

            # Default to first required skill if none found in question
            if not relevant_skill and required_skills:
                relevant_skill = required_skills[0]

            if relevant_skill:
                return web_search_service.get_technical_context(
                    topic=relevant_skill,
                    job_title=job_title
                )
        except Exception as e:
            logger.warning(f"Web search context failed: {e}")

        return None

    def _nlp_only_evaluation(
        self,
        nlp_result: dict,
        skill_coverage: float,
        required_skills: list
    ) -> dict:
        """
        Fallback evaluation using only local NLP analysis.
        No API calls needed.
        """
        base_score = nlp_result["score"]

        # Boost score if required skills are mentioned
        skill_bonus = int(skill_coverage * 15)
        final_score = min(100, base_score + skill_bonus)

        # Generate feedback based on metrics
        feedback = self._generate_nlp_feedback(
            nlp_result, skill_coverage, required_skills
        )

        strengths = []
        improvements = []

        if nlp_result["word_count"] >= 50:
            strengths.append("Good answer length with sufficient detail")
        if skill_coverage >= 0.5:
            strengths.append("Referenced relevant technical skills")
        if nlp_result["vocabulary_diversity"] > 0.7:
            strengths.append("Good vocabulary and varied language")

        if nlp_result["word_count"] < 50:
            improvements.append(
                "Expand your answer with more detail and examples"
            )
        if skill_coverage < 0.3:
            mentioned = ", ".join(required_skills[:2]) if required_skills else "required skills"
            improvements.append(
                f"Mention specific technologies like {mentioned}"
            )
        if nlp_result["sentence_count"] < 3:
            improvements.append(
                "Structure your answer with multiple clear sentences"
            )

        return {
            "score": final_score,
            "feedback": feedback,
            "strengths": strengths,
            "improvements": improvements,
            "nlp_analysis": nlp_result,
            "evaluation_method": "nlp_only"
        }

    def _blend_scores(
        self,
        ai_score: int,
        nlp_score: int,
        skill_coverage: float
    ) -> int:
        """
        Blend AI score with NLP score for a balanced result.
        AI score weighted 70%, NLP score 20%, skill coverage 10%.
        """
        skill_score = int(skill_coverage * 100)
        blended = (
            (ai_score * 0.70) +
            (nlp_score * 0.20) +
            (skill_score * 0.10)
        )
        return min(100, max(0, int(blended)))

    def _generate_nlp_feedback(
        self,
        nlp_result: dict,
        skill_coverage: float,
        required_skills: list
    ) -> str:
        """Generate feedback text based on NLP analysis."""
        word_count = nlp_result["word_count"]

        if word_count < 20:
            return (
                "Your answer was too brief. Aim for at least 50 words "
                "with specific examples from your experience."
            )
        elif word_count < 50:
            return (
                "Your answer covered the basics but needs more depth. "
                "Add specific examples and mention relevant technologies."
            )
        elif skill_coverage < 0.3:
            skills_str = (
                ", ".join(required_skills[:3])
                if required_skills else "required skills"
            )
            return (
                f"Good answer length. To strengthen it, mention specific "
                f"technologies such as {skills_str}."
            )
        else:
            return (
                "Good answer with relevant content. "
                "Consider adding measurable outcomes or specific "
                "project results to make it even stronger."
            )


# Singleton instance
answer_evaluator = AnswerEvaluator()
