"""
Analytics Service — aggregates user performance data across
interviews, typing sessions, and job applications.

Zero external API calls — pure DB aggregation.
"""
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.interview import Interview, Answer, Question
from app.models.typing_session import TypingSession, JobApplication


class AnalyticsService:
    """Aggregates analytics data for the user dashboard."""

    def get_dashboard_summary(
        self,
        db: Session,
        user_id: int
    ) -> dict:
        """
        Get a complete dashboard summary for the user.

        Returns:
            dict with interview stats, typing stats,
            application stats, and overall progress
        """
        interview_stats = self._get_interview_stats(db, user_id)
        typing_stats = self._get_typing_stats(db, user_id)
        application_stats = self._get_application_stats(db, user_id)

        return {
            "interviews": interview_stats,
            "typing": typing_stats,
            "applications": application_stats,
            "overall_readiness_score": self._calculate_readiness(
                interview_stats, typing_stats
            )
        }

    def get_interview_analytics(
        self,
        db: Session,
        user_id: int
    ) -> dict:
        """
        Get detailed interview performance analytics.

        Returns:
            dict with score trends, category breakdown,
            strongest/weakest areas
        """
        interviews = db.query(Interview).filter(
            Interview.user_id == user_id,
            Interview.status == "completed"
        ).order_by(Interview.created_at.asc()).all()

        if not interviews:
            return {
                "total_completed": 0,
                "average_score": 0.0,
                "best_score": 0.0,
                "score_trend": [],
                "category_breakdown": {},
                "trend": "no_data"
            }

        scores = [
            i.overall_score for i in interviews
            if i.overall_score is not None
        ]
        avg_score = (
            round(sum(scores) / len(scores), 1) if scores else 0.0
        )
        best_score = round(max(scores), 1) if scores else 0.0

        score_trend = [
            {
                "interview_id": i.id,
                "score": i.overall_score,
                "date": i.created_at.isoformat()
            }
            for i in interviews
        ]

        category_breakdown = self._get_category_breakdown(
            db, user_id
        )

        trend = "stable"
        if len(scores) >= 4:
            early_avg = sum(scores[:2]) / 2
            recent_avg = sum(scores[-2:]) / 2
            if recent_avg > early_avg * 1.1:
                trend = "improving"
            elif recent_avg < early_avg * 0.9:
                trend = "declining"

        return {
            "total_completed": len(interviews),
            "average_score": avg_score,
            "best_score": best_score,
            "score_trend": score_trend,
            "category_breakdown": category_breakdown,
            "trend": trend
        }

    def get_typing_analytics(
        self,
        db: Session,
        user_id: int
    ) -> dict:
        """Get detailed typing performance analytics."""
        sessions = db.query(TypingSession).filter(
            TypingSession.user_id == user_id
        ).order_by(TypingSession.created_at.asc()).all()

        if not sessions:
            return {
                "total_sessions": 0,
                "average_wpm": 0.0,
                "best_wpm": 0.0,
                "average_accuracy": 0.0,
                "wpm_trend": []
            }

        wpms = [s.wpm for s in sessions if s.wpm is not None]
        accuracies = [
            s.accuracy_percentage for s in sessions
            if s.accuracy_percentage is not None
        ]

        wpm_trend = [
            {
                "session_id": s.id,
                "wpm": s.wpm,
                "accuracy": s.accuracy_percentage,
                "date": s.created_at.isoformat()
            }
            for s in sessions
        ]

        return {
            "total_sessions": len(sessions),
            "average_wpm": (
                round(sum(wpms) / len(wpms), 2) if wpms else 0.0
            ),
            "best_wpm": round(max(wpms), 2) if wpms else 0.0,
            "average_accuracy": (
                round(sum(accuracies) / len(accuracies), 2)
                if accuracies else 0.0
            ),
            "wpm_trend": wpm_trend
        }

    def _get_interview_stats(
        self,
        db: Session,
        user_id: int
    ) -> dict:
        """Get summary interview statistics."""
        total = db.query(Interview).filter(
            Interview.user_id == user_id
        ).count()

        completed = db.query(Interview).filter(
            Interview.user_id == user_id,
            Interview.status == "completed"
        ).count()

        avg_score = db.query(
            func.avg(Interview.overall_score)
        ).filter(
            Interview.user_id == user_id,
            Interview.status == "completed"
        ).scalar()

        return {
            "total": total,
            "completed": completed,
            "in_progress": total - completed,
            "average_score": (
                round(float(avg_score), 1) if avg_score else 0.0
            )
        }

    def _get_typing_stats(
        self,
        db: Session,
        user_id: int
    ) -> dict:
        """Get summary typing statistics."""
        total = db.query(TypingSession).filter(
            TypingSession.user_id == user_id
        ).count()

        avg_wpm = db.query(
            func.avg(TypingSession.wpm)
        ).filter(
            TypingSession.user_id == user_id
        ).scalar()

        best_wpm = db.query(
            func.max(TypingSession.wpm)
        ).filter(
            TypingSession.user_id == user_id
        ).scalar()

        return {
            "total_sessions": total,
            "average_wpm": (
                round(float(avg_wpm), 2) if avg_wpm else 0.0
            ),
            "best_wpm": (
                round(float(best_wpm), 2) if best_wpm else 0.0
            )
        }

    def _get_application_stats(
        self,
        db: Session,
        user_id: int
    ) -> dict:
        """Get summary job application statistics."""
        total = db.query(JobApplication).filter(
            JobApplication.user_id == user_id
        ).count()

        by_status = db.query(
            JobApplication.status,
            func.count(JobApplication.id)
        ).filter(
            JobApplication.user_id == user_id
        ).group_by(JobApplication.status).all()

        return {
            "total": total,
            "by_status": {
                status: count for status, count in by_status
            }
        }

    def _get_category_breakdown(
        self,
        db: Session,
        user_id: int
    ) -> dict:
        """Get average score by question category."""
        results = db.query(
            Question.category,
            func.avg(Answer.score)
        ).join(
            Answer, Answer.question_id == Question.id
        ).filter(
            Answer.user_id == user_id
        ).group_by(Question.category).all()

        return {
            category: round(float(avg_score), 1)
            for category, avg_score in results
            if avg_score is not None
        }

    def _calculate_readiness(
        self,
        interview_stats: dict,
        typing_stats: dict
    ) -> int:
        """
        Calculate an overall job-readiness score (0-100)
        combining interview performance and typing speed.

        Weights: interview 70%, typing 30%
        """
        interview_score = interview_stats.get("average_score", 0.0)
        typing_wpm = typing_stats.get("average_wpm", 0.0)

        # Normalize typing WPM to 0-100 scale (60 WPM = 100)
        typing_score = min(100, (typing_wpm / 60) * 100)

        readiness = (interview_score * 0.7) + (typing_score * 0.3)
        return int(min(100, max(0, readiness)))


# Singleton instance
analytics_service = AnalyticsService()
