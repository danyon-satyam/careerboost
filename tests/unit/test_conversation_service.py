import pytest
from unittest.mock import MagicMock, patch
from app.services.conversation_service import ConversationService


class TestConversationService:
    def setup_method(self):
        self.service = ConversationService()

    def test_needs_follow_up_short_answer(self):
        evaluation = {"score": 70}
        result = self.service._needs_follow_up(
            evaluation, "I know Python."
        )
        assert result is True

    def test_needs_follow_up_low_score(self):
        evaluation = {"score": 35}
        result = self.service._needs_follow_up(
            evaluation,
            "I have some experience with Python and I have used it "
            "in a few projects before."
        )
        assert result is True

    def test_no_follow_up_good_answer(self):
        evaluation = {"score": 78}
        answer = (
            "I have been working with Python for 3 years building "
            "REST APIs with FastAPI and SQLAlchemy. I have also worked "
            "on microservices architecture and deployed to GCP Cloud Run."
        )
        result = self.service._needs_follow_up(evaluation, answer)
        assert result is False

    def test_get_transition_first_question(self):
        msg = self.service._get_transition_message(
            question_order=1,
            total_questions=5,
            answered_count=0,
            job_title="Developer",
            question_category="behavioral"
        )
        assert "begin" in msg.lower() or "start" in msg.lower()

    def test_get_transition_last_question(self):
        msg = self.service._get_transition_message(
            question_order=5,
            total_questions=5,
            answered_count=4,
            job_title="Developer",
            question_category="general"
        )
        assert "final" in msg.lower()

    def test_get_wrap_up_message(self):
        msg = self.service._get_wrap_up_message("Python Developer")
        assert "Python Developer" in msg
        assert "thank" in msg.lower()

    def test_build_response_high_score(self):
        msg = self.service._build_response_message(
            evaluation={"score": 85},
            has_follow_up=False
        )
        assert "strong" in msg.lower()

    def test_build_response_with_follow_up(self):
        msg = self.service._build_response_message(
            evaluation={"score": 85},
            has_follow_up=True
        )
        assert "further" in msg.lower() or "explore" in msg.lower()

    def test_get_greeting_fallback_without_ai(self):
        with patch(
            "app.services.conversation_service.gemini_service"
        ) as mock_gemini:
            mock_gemini.is_available.return_value = False

            greeting = self.service.get_interview_greeting(
                job_title="Python Developer",
                candidate_name="Danyon Satyam",
                total_questions=5
            )

        assert "Danyon" in greeting
        assert "Python Developer" in greeting
        assert isinstance(greeting, str)

    def test_get_greeting_uses_ai_when_available(self):
        with patch(
            "app.services.conversation_service.gemini_service"
        ) as mock_gemini:
            mock_gemini.is_available.return_value = True
            mock_gemini.generate_text.return_value = (
                "Welcome Danyon! Ready for your interview?"
            )

            greeting = self.service.get_interview_greeting(
                job_title="Python Developer",
                candidate_name="Danyon Satyam",
                total_questions=5
            )

        assert isinstance(greeting, str)
        assert len(greeting) > 0

    def test_generate_section_intro_technical(self):
        intro = self.service.generate_section_intro(
            "technical", "Python Developer"
        )
        assert "technical" in intro.lower()

    def test_generate_section_intro_behavioral(self):
        intro = self.service.generate_section_intro(
            "behavioral", "Python Developer"
        )
        assert isinstance(intro, str)
        assert len(intro) > 0


class TestConversationIntegration:
    """Integration tests for conversation flow using mocked DB."""

    def test_get_next_question_raises_not_found(self):
        service = ConversationService()
        mock_db = MagicMock()
        mock_db.query.return_value.options.return_value.filter.return_value.first.return_value = None

        from app.core.exceptions import NotFoundError
        with pytest.raises(NotFoundError):
            service.get_next_question(
                db=mock_db,
                interview_id=999,
                user_id=1
            )

    def test_process_answer_raises_not_found(self):
        service = ConversationService()
        mock_db = MagicMock()
        mock_db.query.return_value.options.return_value.filter.return_value.first.return_value = None

        from app.core.exceptions import NotFoundError
        with pytest.raises(NotFoundError):
            service.process_answer(
                db=mock_db,
                interview_id=999,
                user_id=1,
                question_id=1,
                answer_text="Some answer"
            )


class TestConversationHelpers:
    """Tests for all internal helper methods."""

    def setup_method(self):
        self.service = ConversationService()

    def test_needs_follow_up_exactly_20_words(self):
        """Boundary: exactly 20 words should NOT trigger follow-up."""
        answer = " ".join(["word"] * 20)
        evaluation = {"score": 75}
        result = self.service._needs_follow_up(evaluation, answer)
        assert result is False

    def test_needs_follow_up_19_words(self):
        """Below 20 words always triggers follow-up."""
        answer = " ".join(["word"] * 19)
        evaluation = {"score": 75}
        result = self.service._needs_follow_up(evaluation, answer)
        assert result is True

    def test_needs_follow_up_score_exactly_40(self):
        """Score of 40 does not trigger follow-up."""
        answer = " ".join(["word"] * 30)
        evaluation = {"score": 40}
        result = self.service._needs_follow_up(evaluation, answer)
        assert result is False

    def test_needs_follow_up_score_39(self):
        """Score below 40 triggers follow-up."""
        answer = " ".join(["word"] * 30)
        evaluation = {"score": 39}
        result = self.service._needs_follow_up(evaluation, answer)
        assert result is True

    def test_get_transition_technical_category(self):
        msg = self.service._get_transition_message(
            question_order=3,
            total_questions=5,
            answered_count=2,
            job_title="Developer",
            question_category="technical"
        )
        assert "technical" in msg.lower()

    def test_get_transition_behavioral_category(self):
        msg = self.service._get_transition_message(
            question_order=2,
            total_questions=5,
            answered_count=1,
            job_title="Developer",
            question_category="behavioral"
        )
        assert isinstance(msg, str)
        assert len(msg) > 0

    def test_get_transition_general_category(self):
        msg = self.service._get_transition_message(
            question_order=2,
            total_questions=5,
            answered_count=1,
            job_title="Developer",
            question_category="general"
        )
        assert isinstance(msg, str)

    def test_build_response_medium_score(self):
        msg = self.service._build_response_message(
            evaluation={"score": 65},
            has_follow_up=False
        )
        assert "thank you" in msg.lower()

    def test_build_response_low_score(self):
        msg = self.service._build_response_message(
            evaluation={"score": 40},
            has_follow_up=False
        )
        assert isinstance(msg, str)
        assert len(msg) > 0

    def test_generate_section_intro_general(self):
        intro = self.service.generate_section_intro(
            "general", "Developer"
        )
        assert isinstance(intro, str)
        assert len(intro) > 0

    def test_generate_section_intro_unknown(self):
        intro = self.service.generate_section_intro(
            "unknown_section", "Developer"
        )
        assert isinstance(intro, str)

    def test_get_greeting_fallback_uses_first_name(self):
        with patch(
            "app.services.conversation_service.gemini_service"
        ) as mock_gemini:
            mock_gemini.is_available.return_value = False
            greeting = self.service.get_interview_greeting(
                job_title="Python Developer",
                candidate_name="Danyon Satyam",
                total_questions=5
            )
        assert "Danyon" in greeting
        assert "5" in greeting

    def test_get_greeting_ai_fallback_on_error(self):
        with patch(
            "app.services.conversation_service.gemini_service"
        ) as mock_gemini:
            mock_gemini.is_available.return_value = True
            mock_gemini.generate_text.side_effect = Exception(
                "API error"
            )
            greeting = self.service.get_interview_greeting(
                job_title="Python Developer",
                candidate_name="Satyam",
                total_questions=3
            )
        assert "Satyam" in greeting
        assert isinstance(greeting, str)
