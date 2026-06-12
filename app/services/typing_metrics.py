"""
Typing Metrics Service — calculates WPM, accuracy, and errors
for the typing practice platform inspired by Monkeytype.

Zero API calls — pure math, completely free.
"""
from typing import Optional


# Sample texts for typing practice
TYPING_TEXTS = {
    "easy": [
        (
            "The quick brown fox jumps over the lazy dog. "
            "Practice makes perfect when it comes to typing speed. "
            "Keep your fingers on the home row keys for best results."
        ),
        (
            "Learning to type faster takes consistent daily practice. "
            "Start slow and focus on accuracy before increasing speed. "
            "Your fingers will naturally find the right keys over time."
        ),
        (
            "A good typist can type over eighty words per minute. "
            "Touch typing means you do not look at the keyboard. "
            "This skill is very useful in any professional career."
        ),
    ],
    "medium": [
        (
            "Software development requires strong communication skills "
            "in addition to technical expertise. Writing clean code "
            "that others can understand is just as important as "
            "making it work correctly the first time."
        ),
        (
            "FastAPI is a modern web framework for building APIs "
            "with Python based on standard type hints. It has "
            "automatic interactive documentation and is one of "
            "the fastest Python frameworks available today."
        ),
        (
            "Test-driven development is a software development "
            "process where you write tests before writing the "
            "actual code. This approach helps you think clearly "
            "about what your code needs to accomplish."
        ),
    ],
    "hard": [
        (
            "Asynchronous programming with async/await in Python "
            "allows multiple tasks to run concurrently without "
            "blocking the event loop. This is particularly useful "
            "for I/O-bound operations like database queries, "
            "HTTP requests, and file system operations."
        ),
        (
            "PostgreSQL supports advanced features like JSONB columns, "
            "full-text search, window functions, and common table "
            "expressions. SQLAlchemy's ORM layer abstracts these "
            "features into Python objects while maintaining "
            "excellent performance through connection pooling."
        ),
        (
            "Containerization with Docker allows applications to run "
            "consistently across different environments. Kubernetes "
            "orchestrates multiple containers and handles scaling, "
            "load balancing, and self-healing of failed instances "
            "in a production cluster."
        ),
    ],
    "code": [
        (
            "def calculate_wpm(words_typed, time_seconds):\n"
            "    minutes = time_seconds / 60\n"
            "    return round(words_typed / minutes, 2)\n\n"
            "def calculate_accuracy(correct, total):\n"
            "    return round((correct / total) * 100, 2)"
        ),
        (
            "from fastapi import FastAPI, Depends\n"
            "from sqlalchemy.orm import Session\n\n"
            "app = FastAPI(title='CareerBoost API')\n\n"
            "@app.get('/health')\n"
            "def health_check():\n"
            "    return {'status': 'ok'}"
        ),
    ]
}


class TypingMetricsService:
    """
    Calculates typing performance metrics.

    Metrics:
    - WPM: words per minute (standard = 5 chars per word)
    - Accuracy: percentage of correctly typed characters
    - Errors: count of incorrect characters
    - Consistency: how steady the typing speed was
    """

    def calculate_metrics(
        self,
        test_text: str,
        submitted_text: str,
        time_taken_seconds: int
    ) -> dict:
        """
        Calculate all typing metrics from a completed session.

        Args:
            test_text: The original text the user was asked to type
            submitted_text: What the user actually typed
            time_taken_seconds: Total time in seconds

        Returns:
            dict with wpm, accuracy_percentage, errors_count,
            correct_chars, total_chars
        """
        if time_taken_seconds <= 0:
            time_taken_seconds = 1

        # Character-level comparison
        errors = self._count_errors(test_text, submitted_text)
        total_chars = len(test_text)
        correct_chars = max(0, total_chars - errors)

        # Accuracy calculation
        accuracy = (
            round((correct_chars / total_chars) * 100, 2)
            if total_chars > 0 else 0.0
        )

        # WPM calculation (standard: 5 chars = 1 word)
        typed_chars = len(submitted_text)
        correct_words = max(0, (typed_chars - errors)) / 5
        minutes = time_taken_seconds / 60
        wpm = round(correct_words / minutes, 2) if minutes > 0 else 0.0

        # Performance level
        level = self._get_performance_level(wpm, accuracy)

        return {
            "wpm": wpm,
            "accuracy_percentage": accuracy,
            "errors_count": errors,
            "correct_chars": correct_chars,
            "total_chars": total_chars,
            "typed_chars": typed_chars,
            "time_taken_seconds": time_taken_seconds,
            "performance_level": level,
            "feedback": self._generate_feedback(wpm, accuracy)
        }

    def get_test_text(
        self,
        difficulty: str = "medium",
        category: Optional[str] = None
    ) -> str:
        """
        Get a random typing test text.

        Args:
            difficulty: easy, medium, hard, code
            category: optional specific category

        Returns:
            Text string to type
        """
        import random

        diff = difficulty.lower()
        if diff not in TYPING_TEXTS:
            diff = "medium"

        texts = TYPING_TEXTS[diff]
        return random.choice(texts)

    def _count_errors(
        self,
        original: str,
        typed: str
    ) -> int:
        """
        Count character-level errors between original and typed text.
        Uses edit-distance style comparison.
        """
        errors = 0
        orig_len = len(original)
        typed_len = len(typed)

        # Compare character by character up to the shorter length
        min_len = min(orig_len, typed_len)
        for i in range(min_len):
            if original[i] != typed[i]:
                errors += 1

        # Any missing characters count as errors
        errors += abs(orig_len - typed_len)

        return errors

    def _get_performance_level(
        self,
        wpm: float,
        accuracy: float
    ) -> str:
        """Classify performance level based on WPM and accuracy."""
        if accuracy < 90:
            return "needs_improvement"
        elif wpm < 30:
            return "beginner"
        elif wpm < 50:
            return "intermediate"
        elif wpm < 70:
            return "advanced"
        else:
            return "expert"

    def _generate_feedback(
        self,
        wpm: float,
        accuracy: float
    ) -> str:
        """Generate motivational feedback based on performance."""
        if accuracy < 85:
            return (
                "Focus on accuracy first — slow down and type each "
                "character carefully. Speed will come naturally."
            )
        elif wpm < 30:
            return (
                "Good start! Keep practicing daily to build muscle "
                "memory. Try to maintain a steady rhythm."
            )
        elif wpm < 50:
            return (
                "Solid performance! You are developing good typing "
                "habits. Focus on problem keys to improve further."
            )
        elif wpm < 70:
            return (
                "Great typing speed! You are well above average. "
                "Keep pushing for consistency across all sessions."
            )
        else:
            return (
                "Excellent! You are typing at a professional level. "
                "Your speed and accuracy are impressive."
            )

    def calculate_progress(
        self,
        sessions: list
    ) -> dict:
        """
        Calculate progress across multiple typing sessions.

        Args:
            sessions: list of session dicts with wpm and accuracy

        Returns:
            dict with average, best, trend, improvement
        """
        if not sessions:
            return {
                "average_wpm": 0.0,
                "best_wpm": 0.0,
                "average_accuracy": 0.0,
                "total_sessions": 0,
                "trend": "no_data"
            }

        wpms = [s.get("wpm", 0) for s in sessions if s.get("wpm")]
        accuracies = [
            s.get("accuracy_percentage", 0)
            for s in sessions
            if s.get("accuracy_percentage")
        ]

        avg_wpm = round(sum(wpms) / len(wpms), 2) if wpms else 0.0
        best_wpm = round(max(wpms), 2) if wpms else 0.0
        avg_accuracy = (
            round(sum(accuracies) / len(accuracies), 2)
            if accuracies else 0.0
        )

        # Trend: compare last 3 sessions vs first 3
        trend = "stable"
        if len(wpms) >= 6:
            early_avg = sum(wpms[:3]) / 3
            recent_avg = sum(wpms[-3:]) / 3
            if recent_avg > early_avg * 1.1:
                trend = "improving"
            elif recent_avg < early_avg * 0.9:
                trend = "declining"

        return {
            "average_wpm": avg_wpm,
            "best_wpm": best_wpm,
            "average_accuracy": avg_accuracy,
            "total_sessions": len(sessions),
            "trend": trend
        }


# Singleton instance
typing_metrics_service = TypingMetricsService()
