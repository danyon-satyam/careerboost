import pytest
from app.services.typing_metrics import TypingMetricsService


class TestTypingMetrics:
    def setup_method(self):
        self.service = TypingMetricsService()

    def test_calculate_metrics_perfect_typing(self):
        text = "Hello world this is a test"
        result = self.service.calculate_metrics(
            test_text=text,
            submitted_text=text,
            time_taken_seconds=10
        )
        assert result["accuracy_percentage"] == 100.0
        assert result["errors_count"] == 0
        assert result["wpm"] > 0

    def test_calculate_metrics_with_errors(self):
        result = self.service.calculate_metrics(
            test_text="Hello world",
            submitted_text="Hello worXd",
            time_taken_seconds=5
        )
        assert result["errors_count"] >= 1
        assert result["accuracy_percentage"] < 100.0

    def test_calculate_metrics_wpm_formula(self):
        # 50 chars in 30 seconds = 10 words in 0.5 min = 20 wpm
        text = "a" * 50
        result = self.service.calculate_metrics(
            test_text=text,
            submitted_text=text,
            time_taken_seconds=30
        )
        assert result["wpm"] == pytest.approx(20.0, abs=1.0)

    def test_count_errors_no_errors(self):
        errors = self.service._count_errors(
            "hello world", "hello world"
        )
        assert errors == 0

    def test_count_errors_with_errors(self):
        errors = self.service._count_errors(
            "hello world", "hXllo wXrld"
        )
        assert errors == 2

    def test_count_errors_shorter_input(self):
        errors = self.service._count_errors(
            "hello world", "hello"
        )
        assert errors == 6  # 6 missing chars

    def test_performance_level_beginner(self):
        level = self.service._get_performance_level(25, 95)
        assert level == "beginner"

    def test_performance_level_expert(self):
        level = self.service._get_performance_level(75, 98)
        assert level == "expert"

    def test_performance_level_needs_improvement(self):
        level = self.service._get_performance_level(60, 80)
        assert level == "needs_improvement"

    def test_get_test_text_returns_string(self):
        text = self.service.get_test_text("medium")
        assert isinstance(text, str)
        assert len(text) > 20

    def test_get_test_text_invalid_falls_back(self):
        text = self.service.get_test_text("invalid_level")
        assert isinstance(text, str)
        assert len(text) > 0

    def test_calculate_progress_empty(self):
        result = self.service.calculate_progress([])
        assert result["total_sessions"] == 0
        assert result["trend"] == "no_data"

    def test_calculate_progress_improving(self):
        sessions = [
            {"wpm": 30, "accuracy_percentage": 95},
            {"wpm": 32, "accuracy_percentage": 95},
            {"wpm": 31, "accuracy_percentage": 96},
            {"wpm": 38, "accuracy_percentage": 96},
            {"wpm": 40, "accuracy_percentage": 97},
            {"wpm": 42, "accuracy_percentage": 97},
        ]
        result = self.service.calculate_progress(sessions)
        assert result["trend"] == "improving"
        assert result["best_wpm"] == 42.0
        assert result["total_sessions"] == 6

    def test_generate_feedback_accuracy_low(self):
        feedback = self.service._generate_feedback(60, 80)
        assert "accuracy" in feedback.lower()

    def test_generate_feedback_expert(self):
        feedback = self.service._generate_feedback(75, 98)
        assert "excellent" in feedback.lower()

    def test_zero_time_handled(self):
        result = self.service.calculate_metrics(
            test_text="hello world",
            submitted_text="hello world",
            time_taken_seconds=0
        )
        assert result["wpm"] >= 0


class TestTypingIntegration:
    """Integration tests for typing endpoints."""

    def test_get_test_text(self, client):
        response = client.get("/api/v1/typing/test")
        assert response.status_code == 200
        data = response.json()
        assert "text" in data
        assert "difficulty" in data
        assert "word_count" in data

    def test_get_test_text_difficulty(self, client):
        response = client.get("/api/v1/typing/test?difficulty=easy")
        assert response.status_code == 200

    def test_submit_typing_requires_auth(self, client):
        response = client.post(
            "/api/v1/typing/submit",
            json={
                "test_text": "hello world",
                "submitted_text": "hello world",
                "time_taken_seconds": 10
            }
        )
        assert response.status_code == 403

    def test_submit_typing_success(self, client, auth_headers):
        test_text = (
            "The quick brown fox jumps over the lazy dog "
            "and the cat sat on the mat near the door."
        )
        response = client.post(
            "/api/v1/typing/submit",
            json={
                "test_text": test_text,
                "submitted_text": test_text,
                "time_taken_seconds": 30
            },
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["accuracy_percentage"] == 100.0
        assert data["errors_count"] == 0
        assert data["wpm"] > 0
        assert "performance_level" in data
        assert "feedback" in data

    def test_submit_typing_with_errors(self, client, auth_headers):
        response = client.post(
            "/api/v1/typing/submit",
            json={
                "test_text": "hello world test",
                "submitted_text": "hello worXd tXst",
                "time_taken_seconds": 10
            },
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["errors_count"] >= 1
        assert data["accuracy_percentage"] < 100.0

    def test_get_typing_history(self, client, auth_headers):
        # Submit a session first
        client.post(
            "/api/v1/typing/submit",
            json={
                "test_text": "hello world",
                "submitted_text": "hello world",
                "time_taken_seconds": 10
            },
            headers=auth_headers
        )
        response = client.get(
            "/api/v1/typing/history",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_typing_progress(self, client, auth_headers):
        response = client.get(
            "/api/v1/typing/progress",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "average_wpm" in data
        assert "best_wpm" in data
        assert "total_sessions" in data
