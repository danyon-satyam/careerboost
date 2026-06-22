import pytest


class TestJDParse:
    def test_parse_jd_requires_auth(self, client):
        response = client.post(
            "/api/v1/interviews/parse-jd",
            json={"jd_text": "We need a Python developer with 3 years of experience in FastAPI and PostgreSQL."}
        )
        assert response.status_code == 403

    def test_parse_jd_too_short(self, client, auth_headers):
        response = client.post(
            "/api/v1/interviews/parse-jd",
            json={"jd_text": "Short text"},
            headers=auth_headers
        )
        assert response.status_code == 422

    def test_parse_jd_success(self, client, auth_headers):
        jd = (
            "We are looking for a Senior Python Developer to join "
            "our team at TechCorp. You will build REST APIs using "
            "FastAPI and PostgreSQL. Requirements: 3+ years of "
            "experience with Python, FastAPI, PostgreSQL, Docker, "
            "and AWS. Strong understanding of microservices "
            "architecture and CI/CD pipelines required."
        )
        response = client.post(
            "/api/v1/interviews/parse-jd",
            json={"jd_text": jd},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "interview_id" in data
        assert "job_id" in data
        assert "extracted_skills" in data
        assert isinstance(data["extracted_skills"], list)
        assert data["total_questions"] > 0

    def test_parse_jd_with_overrides(self, client, auth_headers):
        jd = (
            "Looking for a software engineer with experience in "
            "Python, React, and PostgreSQL. Must have 2 years of "
            "experience building scalable web applications and "
            "working with REST APIs and cloud platforms like AWS."
        )
        response = client.post(
            "/api/v1/interviews/parse-jd",
            json={
                "jd_text": jd,
                "title": "Full Stack Engineer",
                "company": "StartupCo"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Full Stack Engineer"
        assert data["company"] == "StartupCo"

    def test_parse_jd_extracts_experience(self, client, auth_headers):
        jd = (
            "Senior Backend Engineer needed with minimum 5 years "
            "of experience in Python and distributed systems. "
            "Strong knowledge of PostgreSQL, Redis, and Kafka "
            "required for this role at our growing company."
        )
        response = client.post(
            "/api/v1/interviews/parse-jd",
            json={"jd_text": jd},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["required_experience"] == 5
