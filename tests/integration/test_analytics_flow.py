import pytest


class TestDashboard:
    def test_dashboard_empty(self, client, auth_headers):
        response = client.get(
            "/api/v1/analytics/dashboard",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "interviews" in data
        assert "typing" in data
        assert "applications" in data
        assert "overall_readiness_score" in data
        assert data["interviews"]["total"] == 0
        assert 0 <= data["overall_readiness_score"] <= 100

    def test_dashboard_requires_auth(self, client):
        response = client.get("/api/v1/analytics/dashboard")
        assert response.status_code == 403

    def test_dashboard_after_activity(
        self, client, auth_headers
    ):
        # Create job and complete an interview
        job = client.post(
            "/api/v1/jobs",
            json={
                "title": "Python Developer",
                "company": "TestCo",
                "description": "Build Python APIs",
                "required_skills": ["Python"],
                "required_experience": 1,
                "location": "Remote",
                "job_type": "remote"
            },
            headers=auth_headers
        )
        job_id = job.json()["id"]

        start = client.post(
            "/api/v1/interviews/start",
            json={"job_id": job_id},
            headers=auth_headers
        )
        interview_id = start.json()["id"]
        question_id = start.json()["questions"][0]["id"]

        client.post(
            f"/api/v1/interviews/{interview_id}/submit-answer",
            json={
                "question_id": question_id,
                "answer_text": (
                    "I have solid Python experience building "
                    "REST APIs with FastAPI and PostgreSQL "
                    "in production environments."
                ),
                "duration_seconds": 40
            },
            headers=auth_headers
        )
        client.post(
            f"/api/v1/interviews/{interview_id}/end",
            headers=auth_headers
        )

        # Submit a typing session
        client.post(
            "/api/v1/typing/submit",
            json={
                "test_text": "hello world typing test",
                "submitted_text": "hello world typing test",
                "time_taken_seconds": 10
            },
            headers=auth_headers
        )

        response = client.get(
            "/api/v1/analytics/dashboard",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["interviews"]["total"] == 1
        assert data["interviews"]["completed"] == 1
        assert data["typing"]["total_sessions"] == 1


class TestInterviewAnalytics:
    def test_interview_analytics_empty(
        self, client, auth_headers
    ):
        response = client.get(
            "/api/v1/analytics/interviews",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total_completed"] == 0
        assert data["trend"] == "no_data"

    def test_interview_analytics_requires_auth(self, client):
        response = client.get("/api/v1/analytics/interviews")
        assert response.status_code == 403

    def test_interview_analytics_with_data(
        self, client, auth_headers
    ):
        job = client.post(
            "/api/v1/jobs",
            json={
                "title": "Backend Engineer",
                "company": "AnalyticsCo",
                "description": "Build backend services",
                "required_skills": ["Python", "FastAPI"],
                "required_experience": 1,
                "location": "Remote",
                "job_type": "remote"
            },
            headers=auth_headers
        )
        job_id = job.json()["id"]

        start = client.post(
            "/api/v1/interviews/start",
            json={"job_id": job_id},
            headers=auth_headers
        )
        interview_id = start.json()["id"]

        client.post(
            f"/api/v1/interviews/{interview_id}/end",
            headers=auth_headers
        )

        response = client.get(
            "/api/v1/analytics/interviews",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total_completed"] >= 1
        assert "score_trend" in data
        assert "category_breakdown" in data


class TestTypingAnalytics:
    def test_typing_analytics_empty(
        self, client, auth_headers
    ):
        response = client.get(
            "/api/v1/analytics/typing",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total_sessions"] == 0
        assert data["wpm_trend"] == []

    def test_typing_analytics_requires_auth(self, client):
        response = client.get("/api/v1/analytics/typing")
        assert response.status_code == 403

    def test_typing_analytics_with_data(
        self, client, auth_headers
    ):
        client.post(
            "/api/v1/typing/submit",
            json={
                "test_text": "the quick brown fox jumps",
                "submitted_text": "the quick brown fox jumps",
                "time_taken_seconds": 8
            },
            headers=auth_headers
        )

        response = client.get(
            "/api/v1/analytics/typing",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total_sessions"] >= 1
        assert data["average_wpm"] > 0
        assert len(data["wpm_trend"]) >= 1
