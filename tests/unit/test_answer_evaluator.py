import pytest
from unittest.mock import patch, MagicMock
from app.services.answer_evaluator import AnswerEvaluator


class TestAnswerEvaluator:
    def setup_method(self):
        self.evaluator = AnswerEvaluator()

    def test_evaluate_too_short_answer(self):
        """Answers under 10 words get score 20 immediately."""
        result = self.evaluator.evaluate(
            question_text="Tell me about yourself",
            answer_text="I like Python.",
            job_title="Developer",
            required_skills=["Python"]
        )
        assert result["score"] == 20
        assert result["evaluation_method"] == "nlp_only"

    def test_evaluate_nlp_only_when_ai_disabled(self):
        result = self.evaluator.evaluate(
            question_text="Tell me about yourself",
            answer_text=(
                "I have been working with Python for 2 years "
                "building REST APIs with FastAPI and PostgreSQL."
            ),
            job_title="Python Developer",
            required_skills=["Python", "FastAPI"],
            use_ai=False
        )
        assert "score" in result
        assert "feedback" in result
        assert result["evaluation_method"] == "nlp_only"
        assert 0 <= result["score"] <= 100

    def test_evaluate_returns_correct_structure(self):
        result = self.evaluator.evaluate(
            question_text="Tell me about Python",
            answer_text=(
                "I have used Python extensively in my projects. "
                "I built REST APIs with FastAPI and SQLAlchemy. "
                "I also worked with PostgreSQL for database management."
            ),
            job_title="Python Developer",
            required_skills=["Python", "FastAPI"],
            use_ai=False
        )
        assert "score" in result
        assert "feedback" in result
        assert "strengths" in result
        assert "improvements" in result
        assert "nlp_analysis" in result
        assert "evaluation_method" in result

    def test_evaluate_with_ai_uses_gemini(self):
        mock_ai_result = {
            "score": 80,
            "feedback": "Excellent answer with clear examples.",
            "strengths": ["Technical depth"],
            "improvements": ["Add more metrics"]
        }
        with patch(
            "app.services.answer_evaluator.gemini_service"
        ) as mock_gemini:
            mock_gemini.is_available.return_value = True
            mock_gemini.evaluate_answer.return_value = mock_ai_result

            with patch(
                "app.services.answer_evaluator.web_search_service"
            ) as mock_search:
                mock_search.get_technical_context.return_value = (
                    "Python is widely used for APIs"
                )

                result = self.evaluator.evaluate(
                    question_text="Tell me about Python APIs",
                    answer_text=(
                        "I built REST APIs with FastAPI and Python. "
                        "I used SQLAlchemy for ORM and PostgreSQL "
                        "for the database. The API handled 1000 "
                        "requests per second in production."
                    ),
                    job_title="Python Developer",
                    required_skills=["Python", "FastAPI"],
                    use_ai=True
                )

        assert result["evaluation_method"] == "ai_pipeline"
        assert "score" in result
        assert result["feedback"] == "Excellent answer with clear examples."

    def test_evaluate_falls_back_on_gemini_error(self):
        with patch(
            "app.services.answer_evaluator.gemini_service"
        ) as mock_gemini:
            mock_gemini.is_available.return_value = True
            mock_gemini.evaluate_answer.side_effect = Exception(
                "API error"
            )

            with patch(
                "app.services.answer_evaluator.web_search_service"
            ) as mock_search:
                mock_search.get_technical_context.return_value = None

                result = self.evaluator.evaluate(
                    question_text="Tell me about Python",
                    answer_text=(
                        "I have worked with Python for building APIs "
                        "using FastAPI framework with PostgreSQL database "
                        "for data storage and SQLAlchemy as the ORM layer."
                    ),
                    job_title="Python Developer",
                    required_skills=["Python"],
                    use_ai=True
                )

        # Should fall back gracefully
        assert result["evaluation_method"] == "nlp_only"
        assert 0 <= result["score"] <= 100

    def test_blend_scores(self):
        blended = self.evaluator._blend_scores(
            ai_score=80,
            nlp_score=60,
            skill_coverage=0.8
        )
        assert 0 <= blended <= 100
        # 80*0.7 + 60*0.2 + 80*0.1 = 56 + 12 + 8 = 76
        assert blended == 76

    def test_nlp_only_evaluation_with_skills(self):
        nlp_result = {
            "score": 70,
            "word_count": 60,
            "sentence_count": 4,
            "avg_sentence_length": 15.0,
            "vocabulary_diversity": 0.8,
            "keywords": ["python", "fastapi"]
        }
        result = self.evaluator._nlp_only_evaluation(
            nlp_result=nlp_result,
            skill_coverage=0.8,
            required_skills=["Python", "FastAPI"]
        )
        assert result["score"] >= 70
        assert len(result["strengths"]) > 0
