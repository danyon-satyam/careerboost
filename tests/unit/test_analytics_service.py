import pytest
from unittest.mock import MagicMock
from app.services.analytics_service import AnalyticsService


class TestAnalyticsServiceUnit:
    def setup_method(self):
        self.service = AnalyticsService()

    def test_calculate_readiness_no_data(self):
        readiness = self.service._calculate_readiness(
            {"average_score": 0.0},
            {"average_wpm": 0.0}
        )
        assert readiness == 0

    def test_calculate_readiness_full_score(self):
        readiness = self.service._calculate_readiness(
            {"average_score": 100.0},
            {"average_wpm": 60.0}
        )
        assert readiness == 100

    def test_calculate_readiness_weighted(self):
        # interview 70% weight, typing 30%
        # 80 * 0.7 + 50 * 0.3 = 56 + 15 = 71
        readiness = self.service._calculate_readiness(
            {"average_score": 80.0},
            {"average_wpm": 30.0}  # 30/60*100 = 50
        )
        assert readiness == 71

    def test_calculate_readiness_caps_at_100(self):
        readiness = self.service._calculate_readiness(
            {"average_score": 100.0},
            {"average_wpm": 120.0}  # over 100 normalized
        )
        assert readiness == 100

    def test_get_interview_analytics_empty(self):
        mock_db = MagicMock()
        mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = []

        result = self.service.get_interview_analytics(mock_db, 1)
        assert result["total_completed"] == 0
        assert result["trend"] == "no_data"

    def test_get_typing_analytics_empty(self):
        mock_db = MagicMock()
        mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = []

        result = self.service.get_typing_analytics(mock_db, 1)
        assert result["total_sessions"] == 0
        assert result["wpm_trend"] == []
