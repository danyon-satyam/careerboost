"""
Web Search Service — uses DuckDuckGo to fetch real-time
technical context for answer evaluation.

No API key needed. Free. No rate limits for reasonable use.
"""
from ddgs import DDGS
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class WebSearchService:
    """
    Fetches real-time web search results using DuckDuckGo.

    Used to:
    - Get current best practices for technical topics
    - Verify if candidate's technical claims are accurate
    - Provide context to Gemini for better answer evaluation
    """

    def search(
        self,
        query: str,
        max_results: int = 3
    ) -> list:
        """
        Search DuckDuckGo and return top results.

        Returns list of dicts with:
        - title: str
        - body: str (snippet)
        - href: str (URL)
        """
        try:
            with DDGS() as ddgs:
                results = list(
                    ddgs.text(
                        query,
                        max_results=max_results
                    )
                )
            return results
        except Exception as e:
            logger.warning(f"Web search failed for '{query}': {e}")
            return []

    def get_technical_context(
        self,
        topic: str,
        job_title: str
    ) -> Optional[str]:
        """
        Get concise technical context for a topic.

        Used to give Gemini current information when
        evaluating technical interview answers.

        Returns a short summary string or None if search fails.
        """
        query = f"{topic} {job_title} best practices 2025"

        results = self.search(query, max_results=3)

        if not results:
            return None

        # Combine snippets into a context string
        context_parts = []
        for r in results:
            body = r.get("body", "").strip()
            if body:
                context_parts.append(body)

        if not context_parts:
            return None

        return " | ".join(context_parts)[:800]

    def search_job_market(
        self,
        job_title: str,
        location: Optional[str] = None
    ) -> list:
        """
        Search for current job market information.
        Used for the job recommendations feature in Week 3.
        """
        location_str = f"in {location}" if location else "India"
        query = f"{job_title} jobs {location_str} 2025 salary skills"
        return self.search(query, max_results=5)

    def verify_technical_claim(
        self,
        claim: str,
        technology: str
    ) -> Optional[str]:
        """
        Verify a technical claim made by the candidate.
        Returns context that Gemini uses for fact-checking.
        """
        query = f"{technology} {claim} documentation"
        results = self.search(query, max_results=2)

        if not results:
            return None

        snippets = [r.get("body", "") for r in results if r.get("body")]
        return " ".join(snippets)[:500] if snippets else None

    def is_available(self) -> bool:
        """Check if web search is available."""
        try:
            self.search("test", max_results=1)
            return True
        except Exception:
            return False


# Singleton instance
web_search_service = WebSearchService()
