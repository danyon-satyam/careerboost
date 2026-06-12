import pytest
from unittest.mock import MagicMock
from app.services.job_matcher import JobMatcherService


class TestJobMatcher:
    def setup_method(self):
        self.service = JobMatcherService()

    def _make_user(
        self,
        skills=None,
        experience_years=2.0,
        summary="",
        target_role=""
    ):
        user = MagicMock()
        user.skills = skills or []
        user.experience_years = experience_years
        user.profile_summary = summary
        user.current_position = ""
        user.target_role = target_role
        return user

    def _make_job(
        self,
        required_skills=None,
        required_experience=2,
        title="Python Developer",
        description="Build APIs"
    ):
        job = MagicMock()
        job.required_skills = required_skills or []
        job.required_experience = required_experience
        job.title = title
        job.description = description
        return job

    def test_skill_match_full_overlap(self):
        result = self.service._calculate_skill_match(
            ["python", "fastapi", "postgresql"],
            ["python", "fastapi", "postgresql"]
        )
        assert result["score"] == 100
        assert result["missing"] == []
        assert len(result["matched"]) == 3

    def test_skill_match_partial_overlap(self):
        result = self.service._calculate_skill_match(
            ["python", "fastapi"],
            ["python", "fastapi", "kubernetes"]
        )
        assert result["score"] == pytest.approx(66, abs=2)
        assert "kubernetes" in result["missing"]

    def test_skill_match_no_overlap(self):
        result = self.service._calculate_skill_match(
            ["java", "spring"],
            ["python", "fastapi"]
        )
        assert result["score"] == 0
        assert len(result["missing"]) == 2

    def test_skill_match_no_requirements(self):
        result = self.service._calculate_skill_match(
            ["python"],
            []
        )
        assert result["score"] == 80

    def test_experience_match_exact(self):
        score = self.service._calculate_experience_match(3.0, 3)
        assert score == 100

    def test_experience_match_over_qualified(self):
        score = self.service._calculate_experience_match(5.0, 2)
        assert score == 100

    def test_experience_match_one_year_short(self):
        score = self.service._calculate_experience_match(2.0, 3)
        assert score == 80

    def test_experience_match_three_years_short(self):
        score = self.service._calculate_experience_match(0.0, 3)
        assert score == 40

    def test_experience_match_no_requirement(self):
        score = self.service._calculate_experience_match(0.0, 0)
        assert score == 100

    def test_get_recommendation_strong(self):
        rec = self.service._get_recommendation(85)
        assert rec == "Strong Match"

    def test_get_recommendation_good(self):
        rec = self.service._get_recommendation(65)
        assert rec == "Good Match"

    def test_get_recommendation_weak(self):
        rec = self.service._get_recommendation(25)
        assert rec == "Weak Match"

    def test_calculate_match_score_full_match(self):
        user = self._make_user(
            skills=["python", "fastapi", "postgresql"],
            experience_years=3.0
        )
        job = self._make_job(
            required_skills=["python", "fastapi", "postgresql"],
            required_experience=2
        )
        result = self.service.calculate_match_score(user, job)
        assert result["match_score"] >= 70
        assert "matched_skills" in result
        assert "missing_skills" in result
        assert "recommendation" in result

    def test_calculate_match_score_no_skills(self):
        user = self._make_user(skills=[], experience_years=0.0)
        job = self._make_job(
            required_skills=["python", "fastapi"],
            required_experience=2
        )
        result = self.service.calculate_match_score(user, job)
        assert result["match_score"] < 50
        assert len(result["missing_skills"]) == 2

    def test_keyword_overlap_score(self):
        score = self.service._keyword_overlap_score(
            "python fastapi postgresql developer",
            "python fastapi developer job"
        )
        assert 0 <= score <= 100
        assert score > 0

    def test_keyword_overlap_empty(self):
        score = self.service._keyword_overlap_score("", "")
        assert score == 50


class TestJobMatchingIntegration:
    def test_get_recommendations_requires_auth(self, client):
        response = client.get("/api/v1/jobs/recommendations")
        assert response.status_code == 403

    def test_get_recommendations_success(
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

    def test_get_match_score_requires_auth(self, client):
        response = client.get("/api/v1/jobs/1/match-score")
        assert response.status_code == 403

    def test_get_match_score_not_found(
        self, client, auth_headers
    ):
        response = client.get(
            "/api/v1/jobs/99999/match-score",
            headers=auth_headers
        )
        assert response.status_code == 404
