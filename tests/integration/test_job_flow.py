import pytest


class TestJobListing:
    def test_get_jobs_returns_list(self, client):
        response = client.get("/api/v1/jobs")
        assert response.status_code == 200
        data = response.json()
        assert "jobs" in data
        assert "total" in data
        assert "page" in data
        assert "page_size" in data

    def test_get_jobs_default_pagination(self, client):
        response = client.get("/api/v1/jobs")
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 1
        assert data["page_size"] == 20

    def test_get_jobs_custom_pagination(self, client):
        response = client.get("/api/v1/jobs?page=2&page_size=5")
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 2
        assert data["page_size"] == 5

    def test_get_jobs_filter_by_location(self, client, auth_headers):
        # Create a job first
        client.post(
            "/api/v1/jobs",
            json={
                "title": "Backend Engineer",
                "company": "TechCorp",
                "description": "Build scalable APIs",
                "location": "Bangalore",
                "required_skills": ["Python", "FastAPI"],
                "required_experience": 2,
                "job_type": "full-time"
            },
            headers=auth_headers
        )
        response = client.get("/api/v1/jobs?location=Bangalore")
        assert response.status_code == 200
        data = response.json()
        assert len(data["jobs"]) >= 1
        assert all(
            "Bangalore" in j["location"]
            for j in data["jobs"]
        )

    def test_get_jobs_filter_by_job_type(self, client, auth_headers):
        client.post(
            "/api/v1/jobs",
            json={
                "title": "Remote Developer",
                "company": "RemoteCo",
                "description": "Work from anywhere",
                "location": "Remote",
                "required_skills": ["React"],
                "required_experience": 1,
                "job_type": "remote"
            },
            headers=auth_headers
        )
        response = client.get("/api/v1/jobs?job_type=remote")
        assert response.status_code == 200
        data = response.json()
        assert len(data["jobs"]) >= 1
        assert all(
            j["job_type"] == "remote"
            for j in data["jobs"]
        )


class TestJobCreate:
    def test_create_job_success(self, client, auth_headers):
        response = client.post(
            "/api/v1/jobs",
            json={
                "title": "Python Developer",
                "company": "StartupXYZ",
                "description": "Build amazing products with Python",
                "location": "Hyderabad",
                "required_skills": ["Python", "Django", "PostgreSQL"],
                "required_experience": 2,
                "salary_min": 800000.0,
                "salary_max": 1200000.0,
                "job_type": "full-time"
            },
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Python Developer"
        assert data["company"] == "StartupXYZ"
        assert "id" in data
        assert data["required_skills"] == [
            "Python", "Django", "PostgreSQL"
        ]

    def test_create_job_requires_auth(self, client):
        response = client.post(
            "/api/v1/jobs",
            json={
                "title": "Python Developer",
                "company": "StartupXYZ",
                "description": "Build amazing products",
                "location": "Hyderabad",
                "required_skills": ["Python"],
                "required_experience": 2,
                "job_type": "full-time"
            }
        )
        assert response.status_code == 403

    def test_create_job_missing_required_fields(
        self, client, auth_headers
    ):
        response = client.post(
            "/api/v1/jobs",
            json={"title": "Incomplete Job"},
            headers=auth_headers
        )
        assert response.status_code == 422


class TestJobDetail:
    def test_get_job_by_id(self, client, auth_headers):
        # Create job first
        create_response = client.post(
            "/api/v1/jobs",
            json={
                "title": "React Developer",
                "company": "WebCo",
                "description": "Build UIs with React",
                "location": "Mumbai",
                "required_skills": ["React", "JavaScript"],
                "required_experience": 1,
                "job_type": "full-time"
            },
            headers=auth_headers
        )
        job_id = create_response.json()["id"]

        response = client.get(f"/api/v1/jobs/{job_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == job_id
        assert data["title"] == "React Developer"

    def test_get_job_not_found(self, client):
        response = client.get("/api/v1/jobs/99999")
        assert response.status_code == 404

    def test_get_similar_jobs(self, client, auth_headers):
        # Create two similar jobs
        r1 = client.post(
            "/api/v1/jobs",
            json={
                "title": "ML Engineer",
                "company": "AI Corp",
                "description": "Build ML models",
                "location": "Pune",
                "required_skills": ["Python", "TensorFlow"],
                "required_experience": 2,
                "job_type": "full-time"
            },
            headers=auth_headers
        )
        client.post(
            "/api/v1/jobs",
            json={
                "title": "Data Scientist",
                "company": "Data Inc",
                "description": "Analyse data",
                "location": "Pune",
                "required_skills": ["Python", "sklearn"],
                "required_experience": 2,
                "job_type": "full-time"
            },
            headers=auth_headers
        )
        job_id = r1.json()["id"]
        response = client.get(f"/api/v1/jobs/{job_id}/similar")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestJobSearch:
    def test_search_jobs_by_keyword(self, client, auth_headers):
        client.post(
            "/api/v1/jobs",
            json={
                "title": "FastAPI Backend Developer",
                "company": "APIFirst",
                "description": "Build REST APIs with FastAPI",
                "location": "Chennai",
                "required_skills": ["FastAPI", "Python"],
                "required_experience": 1,
                "job_type": "full-time"
            },
            headers=auth_headers
        )
        response = client.get("/api/v1/jobs/search?q=FastAPI")
        assert response.status_code == 200
        data = response.json()
        assert "jobs" in data
        assert len(data["jobs"]) >= 1

    def test_search_jobs_no_results(self, client):
        response = client.get(
            "/api/v1/jobs/search?q=xyznonexistentskill123"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["jobs"] == []
        assert data["total"] == 0

    def test_search_jobs_missing_query(self, client):
        response = client.get("/api/v1/jobs/search")
        assert response.status_code == 422
