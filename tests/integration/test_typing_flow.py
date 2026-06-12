import pytest


class TestTypingFlow:
    def test_get_test_text_default(self, client):
        response = client.get("/api/v1/typing/test")
        assert response.status_code == 200
        data = response.json()
        assert "text" in data
        assert "difficulty" in data
        assert "word_count" in data
        assert "char_count" in data
        assert data["difficulty"] == "medium"

    def test_get_test_text_easy(self, client):
        response = client.get("/api/v1/typing/test?difficulty=easy")
        assert response.status_code == 200
        assert response.json()["difficulty"] == "easy"

    def test_get_test_text_hard(self, client):
        response = client.get("/api/v1/typing/test?difficulty=hard")
        assert response.status_code == 200

    def test_get_test_text_code(self, client):
        response = client.get("/api/v1/typing/test?difficulty=code")
        assert response.status_code == 200

    def test_submit_requires_auth(self, client):
        response = client.post(
            "/api/v1/typing/submit",
            json={
                "test_text": "hello world",
                "submitted_text": "hello world",
                "time_taken_seconds": 10
            }
        )
        assert response.status_code == 403

    def test_submit_perfect_typing(self, client, auth_headers):
        test_text = (
            "The quick brown fox jumps over the lazy dog "
            "and the cat sat on the mat near the door today."
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
        assert data["performance_level"] in [
            "beginner", "intermediate", "advanced",
            "expert", "needs_improvement"
        ]
        assert isinstance(data["feedback"], str)

    def test_submit_with_errors(self, client, auth_headers):
        response = client.post(
            "/api/v1/typing/submit",
            json={
                "test_text": "hello world test phrase",
                "submitted_text": "hello worXd tXst phraXe",
                "time_taken_seconds": 10
            },
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["errors_count"] >= 2
        assert data["accuracy_percentage"] < 100.0

    def test_submit_invalid_time(self, client, auth_headers):
        response = client.post(
            "/api/v1/typing/submit",
            json={
                "test_text": "hello world",
                "submitted_text": "hello world",
                "time_taken_seconds": -5
            },
            headers=auth_headers
        )
        assert response.status_code == 422

    def test_submit_empty_text(self, client, auth_headers):
        response = client.post(
            "/api/v1/typing/submit",
            json={
                "test_text": "hello world",
                "submitted_text": "   ",
                "time_taken_seconds": 10
            },
            headers=auth_headers
        )
        assert response.status_code == 422

    def test_history_empty(self, client, auth_headers):
        response = client.get(
            "/api/v1/typing/history",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_history_after_submit(self, client, auth_headers):
        client.post(
            "/api/v1/typing/submit",
            json={
                "test_text": "hello world typing test",
                "submitted_text": "hello world typing test",
                "time_taken_seconds": 15
            },
            headers=auth_headers
        )
        response = client.get(
            "/api/v1/typing/history",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1

    def test_history_requires_auth(self, client):
        response = client.get("/api/v1/typing/history")
        assert response.status_code == 403

    def test_progress_empty(self, client, auth_headers):
        response = client.get(
            "/api/v1/typing/progress",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "average_wpm" in data
        assert "best_wpm" in data
        assert "total_sessions" in data
        assert "trend" in data

    def test_progress_requires_auth(self, client):
        response = client.get("/api/v1/typing/progress")
        assert response.status_code == 403

    def test_progress_after_multiple_sessions(
        self, client, auth_headers
    ):
        texts = [
            "hello world practice",
            "python fastapi development",
            "typing speed accuracy test"
        ]
        for text in texts:
            client.post(
                "/api/v1/typing/submit",
                json={
                    "test_text": text,
                    "submitted_text": text,
                    "time_taken_seconds": 10
                },
                headers=auth_headers
            )

        response = client.get(
            "/api/v1/typing/progress",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total_sessions"] >= 3
        assert data["best_wpm"] > 0


class TestJobMatchingFlow:
    def test_recommendations_requires_auth(self, client):
        response = client.get("/api/v1/jobs/recommendations")
        assert response.status_code == 403

    def test_recommendations_empty_profile(
        self, client, auth_headers
    ):
        response = client.get(
            "/api/v1/jobs/recommendations",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "recommendations" in data
        assert "total" in data
        assert "user_skills_count" in data

    def test_recommendations_with_skills(
        self, client, auth_headers
    ):
        # Update profile with skills first
        client.patch(
            "/api/v1/users/profile",
            json={
                "skills": ["python", "fastapi", "postgresql"],
                "experience_years": 2.0,
                "target_role": "Backend Engineer"
            },
            headers=auth_headers
        )

        # Create a matching job
        client.post(
            "/api/v1/jobs",
            json={
                "title": "Python Backend Engineer",
                "company": "MatchCorp",
                "description": "Build APIs with Python FastAPI",
                "required_skills": ["python", "fastapi"],
                "required_experience": 2,
                "location": "Bangalore",
                "job_type": "full-time"
            },
            headers=auth_headers
        )

        response = client.get(
            "/api/v1/jobs/recommendations",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["user_skills_count"] == 3

    def test_match_score_requires_auth(self, client):
        response = client.get("/api/v1/jobs/1/match-score")
        assert response.status_code == 403

    def test_match_score_not_found(
        self, client, auth_headers
    ):
        response = client.get(
            "/api/v1/jobs/99999/match-score",
            headers=auth_headers
        )
        assert response.status_code == 404

    def test_match_score_returns_breakdown(
        self, client, auth_headers
    ):
        # Create a job
        create = client.post(
            "/api/v1/jobs",
            json={
                "title": "Python Developer",
                "company": "TestCo",
                "description": "Build Python APIs",
                "required_skills": ["python", "fastapi"],
                "required_experience": 1,
                "location": "Remote",
                "job_type": "remote"
            },
            headers=auth_headers
        )
        job_id = create.json()["id"]

        response = client.get(
            f"/api/v1/jobs/{job_id}/match-score",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "match_score" in data
        assert "matched_skills" in data
        assert "missing_skills" in data
        assert "recommendation" in data
        assert "skill_score" in data
        assert "experience_score" in data
        assert 0 <= data["match_score"] <= 100
