import pytest
from unittest.mock import patch, MagicMock
from app.services.gemini_service import GeminiService


class TestGeminiService:
    def setup_method(self):
        self.service = GeminiService()

    def test_is_available_false_when_no_key(self):
        with patch(
            "app.services.gemini_service.settings"
        ) as mock_settings:
            mock_settings.GEMINI_API_KEY = None
            service = GeminiService()
            assert service.is_available() is False

    def test_is_available_true_when_key_set(self):
        with patch(
            "app.services.gemini_service.settings"
        ) as mock_settings:
            mock_settings.GEMINI_API_KEY = "fake-key-123"
            service = GeminiService()
            assert service.is_available() is True

    def test_generate_text_raises_without_key(self):
        with patch(
            "app.services.gemini_service.settings"
        ) as mock_settings:
            mock_settings.GEMINI_API_KEY = None
            service = GeminiService()
            with pytest.raises(ValueError, match="GEMINI_API_KEY"):
                service.generate_text("test prompt")

    def test_evaluate_answer_structure(self):
        """Test that evaluate_answer returns correct structure."""
        mock_response = (
            '{"score": 75, "feedback": "Good answer.", '
            '"strengths": ["Clear"], "improvements": ["Add examples"]}'
        )
        with patch.object(
            self.service, "generate_text", return_value=mock_response
        ):
            result = self.service.evaluate_answer(
                question_text="Tell me about Python",
                answer_text="Python is a programming language I use daily",
                job_title="Python Developer",
                required_skills=["Python"]
            )
            assert "score" in result
            assert "feedback" in result
            assert "strengths" in result
            assert "improvements" in result
            assert 0 <= result["score"] <= 100

    def test_generate_interview_questions_structure(self):
        """Test that question generation returns correct structure."""
        mock_response = '''[
            {
                "question_text": "Tell me about yourself",
                "category": "behavioral",
                "difficulty": 1,
                "expected_duration_seconds": 120
            },
            {
                "question_text": "Explain REST APIs",
                "category": "technical",
                "difficulty": 3,
                "expected_duration_seconds": 150
            }
        ]'''
        with patch.object(
            self.service, "generate_text", return_value=mock_response
        ):
            questions = self.service.generate_interview_questions(
                job_title="Python Developer",
                job_description="Build REST APIs",
                required_skills=["Python", "FastAPI"],
                num_questions=2
            )
            assert isinstance(questions, list)
            assert len(questions) == 2
            for q in questions:
                assert "question_text" in q
                assert "category" in q
                assert "difficulty" in q
                assert 1 <= q["difficulty"] <= 5

    def test_generate_follow_up_returns_string(self):
        with patch.object(
            self.service,
            "generate_text",
            return_value="Can you elaborate on that?"
        ):
            result = self.service.generate_follow_up_question(
                original_question="Tell me about Python",
                candidate_answer="I use Python for APIs",
                job_title="Developer"
            )
            assert isinstance(result, str)
            assert len(result) > 0
