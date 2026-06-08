import pytest


@pytest.fixture(scope="function")
def sample_job(client, auth_headers):
    """Creates a sample job for interview tests."""
    response = client.post(
        "/api/v1/jobs",
        json={
            "title": "Python Developer",
            "company": "TestCorp",
            "description": "Build APIs with Python and FastAPI",
            "required_skills": ["Python", "FastAPI", "PostgreSQL"],
            "required_experience": 2,
            "location": "Bangalore",
            "job_type": "full-time"
        },
        headers=auth_headers
    )
    assert response.status_code == 201
    return response.json()


class TestStartInterview:
    def test_start_interview_success(
        self, client, auth_headers, sample_job
    ):
        response = client.post(
            "/api/v1/interviews/start",
            json={"job_id": sample_job["id"]},
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "in-progress"
        assert data["job_id"] == sample_job["id"]
        assert "id" in data
        assert "questions" in data
        assert len(data["questions"]) > 0

    def test_start_interview_requires_auth(
        self, client, sample_job
    ):
        response = client.post(
            "/api/v1/interviews/start",
            json={"job_id": sample_job["id"]}
        )
        assert response.status_code == 403

    def test_start_interview_invalid_job(
        self, client, auth_headers
    ):
        response = client.post(
            "/api/v1/interviews/start",
            json={"job_id": 99999},
            headers=auth_headers
        )
        assert response.status_code == 404

    def test_start_interview_missing_job_id(
        self, client, auth_headers
    ):
        response = client.post(
            "/api/v1/interviews/start",
            json={},
            headers=auth_headers
        )
        assert response.status_code == 422


class TestGetInterview:
    def test_get_interview_by_id(
        self, client, auth_headers, sample_job
    ):
        # Start interview first
        start = client.post(
            "/api/v1/interviews/start",
            json={"job_id": sample_job["id"]},
            headers=auth_headers
        )
        interview_id = start.json()["id"]

        response = client.get(
            f"/api/v1/interviews/{interview_id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == interview_id
        assert data["status"] == "in-progress"

    def test_get_interview_not_found(
        self, client, auth_headers
    ):
        response = client.get(
            "/api/v1/interviews/99999",
            headers=auth_headers
        )
        assert response.status_code == 404

    def test_get_interview_requires_auth(
        self, client, auth_headers, sample_job
    ):
        start = client.post(
            "/api/v1/interviews/start",
            json={"job_id": sample_job["id"]},
            headers=auth_headers
        )
        interview_id = start.json()["id"]

        response = client.get(
            f"/api/v1/interviews/{interview_id}"
        )
        assert response.status_code == 403

    def test_list_user_interviews(
        self, client, auth_headers, sample_job
    ):
        # Start an interview
        client.post(
            "/api/v1/interviews/start",
            json={"job_id": sample_job["id"]},
            headers=auth_headers
        )
        response = client.get(
            "/api/v1/interviews",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1


class TestSubmitAnswer:
    def test_submit_answer_success(
        self, client, auth_headers, sample_job
    ):
        # Start interview
        start = client.post(
            "/api/v1/interviews/start",
            json={"job_id": sample_job["id"]},
            headers=auth_headers
        )
        interview_id = start.json()["id"]
        question_id = start.json()["questions"][0]["id"]

        response = client.post(
            f"/api/v1/interviews/{interview_id}/submit-answer",
            json={
                "question_id": question_id,
                "answer_text": (
                    "I have 2 years of experience with Python. "
                    "I have built REST APIs using FastAPI and SQLAlchemy."
                ),
                "duration_seconds": 45
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "score" in data
        assert "feedback" in data
        assert 0 <= data["score"] <= 100

    def test_submit_answer_requires_auth(
        self, client, auth_headers, sample_job
    ):
        start = client.post(
            "/api/v1/interviews/start",
            json={"job_id": sample_job["id"]},
            headers=auth_headers
        )
        interview_id = start.json()["id"]
        question_id = start.json()["questions"][0]["id"]

        response = client.post(
            f"/api/v1/interviews/{interview_id}/submit-answer",
            json={
                "question_id": question_id,
                "answer_text": "Some answer",
                "duration_seconds": 30
            }
        )
        assert response.status_code == 403

    def test_submit_answer_missing_fields(
        self, client, auth_headers, sample_job
    ):
        start = client.post(
            "/api/v1/interviews/start",
            json={"job_id": sample_job["id"]},
            headers=auth_headers
        )
        interview_id = start.json()["id"]

        response = client.post(
            f"/api/v1/interviews/{interview_id}/submit-answer",
            json={},
            headers=auth_headers
        )
        assert response.status_code == 422


class TestEndInterview:
    def test_end_interview_success(
        self, client, auth_headers, sample_job
    ):
        start = client.post(
            "/api/v1/interviews/start",
            json={"job_id": sample_job["id"]},
            headers=auth_headers
        )
        interview_id = start.json()["id"]

        response = client.post(
            f"/api/v1/interviews/{interview_id}/end",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"

    def test_end_interview_requires_auth(
        self, client, auth_headers, sample_job
    ):
        start = client.post(
            "/api/v1/interviews/start",
            json={"job_id": sample_job["id"]},
            headers=auth_headers
        )
        interview_id = start.json()["id"]

        response = client.post(
            f"/api/v1/interviews/{interview_id}/end"
        )
        assert response.status_code == 403


class TestInterviewResults:
    def test_get_results_success(
        self, client, auth_headers, sample_job
    ):
        # Start and end interview
        start = client.post(
            "/api/v1/interviews/start",
            json={"job_id": sample_job["id"]},
            headers=auth_headers
        )
        interview_id = start.json()["id"]
        client.post(
            f"/api/v1/interviews/{interview_id}/end",
            headers=auth_headers
        )

        response = client.get(
            f"/api/v1/interviews/{interview_id}/results",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "overall_score" in data
        assert "feedback_text" in data
        assert "status" in data
        assert data["status"] == "completed"

    def test_get_results_requires_auth(
        self, client, auth_headers, sample_job
    ):
        start = client.post(
            "/api/v1/interviews/start",
            json={"job_id": sample_job["id"]},
            headers=auth_headers
        )
        interview_id = start.json()["id"]

        response = client.get(
            f"/api/v1/interviews/{interview_id}/results"
        )
        assert response.status_code == 403
