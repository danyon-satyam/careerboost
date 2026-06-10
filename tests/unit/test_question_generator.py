import pytest
from unittest.mock import patch
from app.services.question_generator import QuestionGenerator


class TestQuestionGenerator:
    def setup_method(self):
        self.generator = QuestionGenerator()

    def test_generate_falls_back_when_ai_unavailable(self):
        with patch(
            "app.services.question_generator.gemini_service"
        ) as mock_gemini:
            mock_gemini.is_available.return_value = False

            questions = self.generator.generate_questions(
                job_title="Python Developer",
                job_description="Build APIs",
                required_skills=["Python"],
                num_questions=3
            )

        assert isinstance(questions, list)
        assert len(questions) == 3
        for q in questions:
            assert "question_text" in q
            assert "category" in q
            assert "difficulty" in q

    def test_generate_uses_ai_when_available(self):
        mock_questions = [
            {
                "question_text": "Tell me about Python",
                "category": "technical",
                "difficulty": 2,
                "expected_duration_seconds": 120,
                "question_order": 1
            },
            {
                "question_text": "Describe a project",
                "category": "behavioral",
                "difficulty": 1,
                "expected_duration_seconds": 90,
                "question_order": 2
            }
        ]
        with patch(
            "app.services.question_generator.gemini_service"
        ) as mock_gemini:
            mock_gemini.is_available.return_value = True
            mock_gemini.generate_interview_questions.return_value = (
                mock_questions
            )

            questions = self.generator.generate_questions(
                job_title="Python Developer",
                job_description="Build REST APIs",
                required_skills=["Python", "FastAPI"],
                num_questions=2
            )

        assert len(questions) == 2
        assert questions[0]["question_text"] == "Tell me about Python"

    def test_generate_falls_back_on_ai_error(self):
        with patch(
            "app.services.question_generator.gemini_service"
        ) as mock_gemini:
            mock_gemini.is_available.return_value = True
            mock_gemini.generate_interview_questions.side_effect = (
                Exception("API error")
            )

            questions = self.generator.generate_questions(
                job_title="Python Developer",
                job_description="Build APIs",
                required_skills=["Python"],
                num_questions=5
            )

        assert isinstance(questions, list)
        assert len(questions) == 5

    def test_generate_follow_up_returns_none_without_ai(self):
        with patch(
            "app.services.question_generator.gemini_service"
        ) as mock_gemini:
            mock_gemini.is_available.return_value = False

            result = self.generator.generate_follow_up(
                original_question="Tell me about Python",
                candidate_answer="I use Python daily",
                job_title="Developer"
            )

        assert result is None
