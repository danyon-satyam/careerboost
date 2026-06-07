import pytest
from unittest.mock import MagicMock, patch
from app.services.user_service import UserService
from app.core.exceptions import NotFoundError, ConflictError


class TestUserServiceUnit:
    def setup_method(self):
        self.service = UserService()

    def test_get_by_id_raises_not_found(self):
        mock_db = MagicMock()
        mock_db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(NotFoundError):
            self.service.get_by_id(mock_db, 999)

    def test_get_by_email_returns_none_when_not_found(self):
        mock_db = MagicMock()
        mock_db.query.return_value.filter.return_value.first.return_value = None

        result = self.service.get_by_email(mock_db, "notfound@test.com")
        assert result is None

    def test_delete_user_sets_inactive(self):
        mock_db = MagicMock()
        mock_user = MagicMock()
        mock_user.is_active = True
        mock_db.query.return_value.filter.return_value.first.return_value = mock_user

        result = self.service.delete_user(mock_db, 1)
        assert result is True
        assert mock_user.is_active is False
        mock_db.commit.assert_called_once()
