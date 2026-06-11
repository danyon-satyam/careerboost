import pytest
from app.services.resume_parser import ResumeParser


class TestResumeParser:
    def setup_method(self):
        self.parser = ResumeParser()

    def test_parse_text_returns_correct_structure(self):
        result = self.parser.parse_text(
            "Python developer with 3 years of experience. "
            "Skills: Python, FastAPI, PostgreSQL, Docker, React."
        )
        assert "skills" in result
        assert "experience_years" in result
        assert "education" in result
        assert "summary" in result
        assert "parse_success" in result

    def test_extract_skills_finds_python(self):
        skills = self.parser._extract_skills(
            "experienced python developer using fastapi and postgresql"
        )
        assert "python" in skills
        assert "fastapi" in skills
        assert "postgresql" in skills

    def test_extract_skills_returns_sorted_list(self):
        skills = self.parser._extract_skills(
            "skills: react, python, docker, aws"
        )
        assert skills == sorted(skills)

    def test_extract_experience_direct_mention(self):
        years = self.parser._extract_experience_years(
            "I have 5 years of experience in software development."
        )
        assert years == 5.0

    def test_extract_experience_from_date_ranges(self):
        years = self.parser._extract_experience_years(
            "Software Engineer at TechCorp 2020-2023\n"
            "Junior Dev at StartupXYZ 2019-2020"
        )
        assert years >= 3.0

    def test_extract_experience_returns_zero_when_none(self):
        years = self.parser._extract_experience_years(
            "Recent graduate looking for first job."
        )
        assert years == 0.0

    def test_extract_education_btech(self):
        edu = self.parser._extract_education(
            "b.tech in computer science from xyz university"
        )
        assert edu == "Bachelor's"

    def test_extract_education_masters(self):
        edu = self.parser._extract_education(
            "m.tech in software engineering"
        )
        assert edu == "Master's"

    def test_extract_education_phd(self):
        edu = self.parser._extract_education(
            "phd in artificial intelligence"
        )
        assert edu == "PhD"

    def test_extract_education_not_specified(self):
        edu = self.parser._extract_education(
            "software developer with great skills"
        )
        assert edu == "Not specified"

    def test_extract_email_found(self):
        email = self.parser._extract_email(
            "Contact: danyon@careerboost.com | +91-9876543210"
        )
        assert email == "danyon@careerboost.com"

    def test_extract_email_not_found(self):
        email = self.parser._extract_email(
            "No email address in this text"
        )
        assert email is None

    def test_parse_text_too_short(self):
        result = self.parser.parse_text("Hi")
        assert result["parse_success"] is False
        assert result["skills"] == []

    def test_generate_summary_senior(self):
        summary = self.parser._generate_summary(
            "text", ["python", "fastapi"], 6.0
        )
        assert "Senior" in summary
        assert "6.0" in summary

    def test_generate_summary_junior(self):
        summary = self.parser._generate_summary(
            "text", ["python"], 1.5
        )
        assert "Junior" in summary

    def test_generate_summary_entry_level(self):
        summary = self.parser._generate_summary(
            "text", [], 0.0
        )
        assert "Entry-level" in summary

    def test_empty_result_structure(self):
        result = self.parser._empty_result("Test error")
        assert result["parse_success"] is False
        assert result["skills"] == []
        assert result["experience_years"] == 0.0
        assert result["error"] == "Test error"

    def test_full_parse_text_integration(self):
        resume = """
        John Doe
        john@example.com

        SUMMARY
        Software engineer with 3 years of experience.

        SKILLS
        Python, FastAPI, React, PostgreSQL, Docker, AWS, Git

        EDUCATION
        B.Tech in Computer Science - XYZ University (2018-2022)

        EXPERIENCE
        Software Engineer - TechCorp (2022-2025)
        - Built REST APIs with Python and FastAPI
        - Managed PostgreSQL databases
        - Deployed applications using Docker on AWS
        """
        result = self.parser.parse_text(resume)
        assert result["parse_success"] is True
        assert "python" in result["skills"]
        assert "fastapi" in result["skills"]
        assert result["experience_years"] >= 0
        assert result["education"] == "Bachelor's"
        assert result["email"] == "john@example.com"
