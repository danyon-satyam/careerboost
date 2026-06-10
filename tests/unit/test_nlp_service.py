import pytest
from app.services.nlp_service import NLPService


class TestNLPService:
    def setup_method(self):
        self.nlp = NLPService()

    def test_extract_keywords_returns_list(self):
        keywords = self.nlp.extract_keywords(
            "Python developer with FastAPI experience"
        )
        assert isinstance(keywords, list)

    def test_calculate_skill_coverage_full_match(self):
        coverage = self.nlp.calculate_skill_coverage(
            "I work with Python and FastAPI every day",
            ["Python", "FastAPI"]
        )
        assert coverage == 1.0

    def test_calculate_skill_coverage_partial_match(self):
        coverage = self.nlp.calculate_skill_coverage(
            "I work with Python every day",
            ["Python", "FastAPI"]
        )
        assert coverage == 0.5

    def test_calculate_skill_coverage_no_skills(self):
        coverage = self.nlp.calculate_skill_coverage(
            "Some answer text", []
        )
        assert coverage == 0.0

    def test_get_answer_quality_score_short_answer(self):
        result = self.nlp.get_answer_quality_score("I know Python.")
        assert result["score"] <= 40
        assert result["word_count"] <= 5

    def test_get_answer_quality_score_long_answer(self):
        answer = (
            "I have been working with Python for three years. "
            "During this time I built several REST APIs using FastAPI "
            "and SQLAlchemy. I also worked with React on the frontend "
            "and PostgreSQL for the database. My most recent project "
            "was a complete authentication system with JWT tokens and "
            "refresh token rotation for a production application."
        )
        result = self.nlp.get_answer_quality_score(answer)
        assert result["score"] >= 70
        assert result["word_count"] > 50

    def test_extract_skills_from_text(self):
        skills = self.nlp.extract_skills_from_text(
            "I use Python and React with PostgreSQL"
        )
        assert "python" in skills
        assert "react" in skills
        assert "postgresql" in skills

    def test_count_sentences(self):
        count = self.nlp.count_sentences(
            "This is sentence one. This is sentence two. Third one."
        )
        assert count >= 2

    def test_is_available_returns_bool(self):
        result = self.nlp.is_available()
        assert isinstance(result, bool)
