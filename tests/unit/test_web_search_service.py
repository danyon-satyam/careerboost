import pytest
from unittest.mock import patch, MagicMock
from app.services.web_search_service import WebSearchService


class TestWebSearchService:
    def setup_method(self):
        self.service = WebSearchService()

    def test_search_returns_list(self):
        mock_results = [
            {
                "title": "FastAPI Best Practices",
                "body": "Use dependency injection for clean code",
                "href": "https://example.com"
            }
        ]
        with patch.object(
            self.service, "search", return_value=mock_results
        ):
            results = self.service.search("FastAPI best practices")
            assert isinstance(results, list)

    def test_get_technical_context_returns_string(self):
        mock_results = [
            {
                "title": "Python REST API",
                "body": "FastAPI is a modern web framework for Python",
                "href": "https://example.com"
            }
        ]
        with patch.object(
            self.service, "search", return_value=mock_results
        ):
            context = self.service.get_technical_context(
                "REST API", "Python Developer"
            )
            assert context is not None
            assert isinstance(context, str)
            assert len(context) > 0

    def test_get_technical_context_returns_none_on_empty(self):
        with patch.object(self.service, "search", return_value=[]):
            context = self.service.get_technical_context(
                "anything", "any role"
            )
            assert context is None

    def test_search_returns_empty_on_failure(self):
        with patch(
            "app.services.web_search_service.DDGS",
            side_effect=Exception("Network error")
        ):
            results = self.service.search("test query")
            assert results == []

    def test_verify_technical_claim_returns_none_on_no_results(self):
        with patch.object(self.service, "search", return_value=[]):
            result = self.service.verify_technical_claim(
                "is fast", "FastAPI"
            )
            assert result is None
