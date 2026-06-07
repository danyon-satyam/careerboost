import pytest
from unittest.mock import MagicMock
from app.services.job_service import JobService
from app.core.exceptions import NotFoundError


class TestJobServiceUnit:
    def setup_method(self):
        self.service = JobService()

    def test_get_by_id_raises_not_found(self):
        mock_db = MagicMock()
        mock_db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(NotFoundError):
            self.service.get_by_id(mock_db, 999)

    def test_deactivate_job_sets_inactive(self):
        mock_db = MagicMock()
        mock_job = MagicMock()
        mock_job.is_active = True
        mock_db.query.return_value.filter.return_value.first.return_value = mock_job

        result = self.service.deactivate_job(mock_db, 1)
        assert result is True
        assert mock_job.is_active is False
        mock_db.commit.assert_called_once()

    def test_search_returns_empty_for_no_match(self):
        mock_db = MagicMock()
        mock_query = MagicMock()
        mock_query.count.return_value = 0
        mock_query.order_by.return_value.offset.return_value.limit.return_value.all.return_value = []
        mock_db.query.return_value.filter.return_value = mock_query

        result = self.service.search(mock_db, "xyznothing")
        assert result["total"] == 0
        assert result["jobs"] == []
        assert result["query"] == "xyznothing"
