"""
Seed script — populates the database with sample data for development.
Run with: python scripts/seed_database.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import SessionLocal
from app.services.user_service import user_service
from app.services.job_service import job_service
from app.core.exceptions import ConflictError


def seed_users(db):
    print("Seeding users...")
    users_data = [
        {
            "email": "candidate1@careerboost.com",
            "password": "Password123!",
            "full_name": "Arjun Sharma"
        },
        {
            "email": "candidate2@careerboost.com",
            "password": "Password123!",
            "full_name": "Priya Nair"
        },
        {
            "email": "recruiter@careerboost.com",
            "password": "Password123!",
            "full_name": "Rahul Mehta"
        },
    ]
    created = []
    for u in users_data:
        try:
            user = user_service.create_user(
                db,
                email=u["email"],
                password=u["password"],
                full_name=u["full_name"]
            )
            # Update with sample profile data
            user_service.update_user(db, user.id, {
                "skills": ["Python", "React", "PostgreSQL"],
                "experience_years": 2.0,
                "target_role": "Full Stack Engineer",
                "current_position": "Student"
            })
            created.append(user)
            print(f"  ✅ Created user: {user.email}")
        except ConflictError:
            print(f"  ⚠️  User already exists: {u['email']}")
    return created


def seed_jobs(db):
    print("Seeding jobs...")
    jobs_data = [
        {
            "title": "Full Stack Engineer",
            "company": "TechStartup India",
            "description": (
                "Build scalable web applications using FastAPI and React. "
                "Work on AI-powered features and RESTful APIs."
            ),
            "required_skills": ["Python", "FastAPI", "React", "PostgreSQL"],
            "required_experience": 2,
            "salary_min": 800000.0,
            "salary_max": 1400000.0,
            "location": "Bangalore",
            "job_type": "full-time",
            "source": "manual"
        },
        {
            "title": "Backend Python Developer",
            "company": "FinTech Solutions",
            "description": (
                "Develop and maintain backend services for financial products. "
                "Strong Python and SQL skills required."
            ),
            "required_skills": ["Python", "Django", "PostgreSQL", "Redis"],
            "required_experience": 3,
            "salary_min": 1000000.0,
            "salary_max": 1800000.0,
            "location": "Hyderabad",
            "job_type": "full-time",
            "source": "manual"
        },
        {
            "title": "React Frontend Developer",
            "company": "Product Company",
            "description": (
                "Create beautiful, responsive UIs using React and Tailwind CSS. "
                "Experience with animations and complex state management preferred."
            ),
            "required_skills": ["React", "JavaScript", "Tailwind CSS", "Redux"],
            "required_experience": 1,
            "salary_min": 600000.0,
            "salary_max": 1000000.0,
            "location": "Pune",
            "job_type": "full-time",
            "source": "manual"
        },
        {
            "title": "ML Engineer",
            "company": "AI Research Lab",
            "description": (
                "Build and deploy machine learning models for NLP tasks. "
                "Experience with Transformers, spaCy, and model serving required."
            ),
            "required_skills": [
                "Python", "TensorFlow", "spaCy",
                "scikit-learn", "FastAPI"
            ],
            "required_experience": 2,
            "salary_min": 1200000.0,
            "salary_max": 2000000.0,
            "location": "Bangalore",
            "job_type": "full-time",
            "source": "manual"
        },
        {
            "title": "Remote DevOps Engineer",
            "company": "Cloud Native Co",
            "description": (
                "Manage CI/CD pipelines, Docker containers, and GCP deployments. "
                "Experience with GitHub Actions and Kubernetes preferred."
            ),
            "required_skills": ["Docker", "GCP", "GitHub Actions", "Python"],
            "required_experience": 2,
            "salary_min": 1000000.0,
            "salary_max": 1600000.0,
            "location": "Remote",
            "job_type": "remote",
            "source": "manual"
        },
        {
            "title": "Python Internship",
            "company": "EdTech Startup",
            "description": (
                "Learn and contribute to a fast-growing EdTech platform. "
                "Basic Python knowledge required. Great mentorship provided."
            ),
            "required_skills": ["Python", "SQL"],
            "required_experience": 0,
            "salary_min": 15000.0,
            "salary_max": 25000.0,
            "location": "Chennai",
            "job_type": "internship",
            "source": "manual"
        },
    ]

    for j in jobs_data:
        job = job_service.create_job(db, j)
        print(f"  ✅ Created job: {job.title} at {job.company}")


def main():
    print("🌱 Starting database seed...\n")
    db = SessionLocal()
    try:
        seed_users(db)
        print()
        seed_jobs(db)
        print("\n✅ Database seeded successfully!")
        print("   3 users and 6 jobs created.")
    except Exception as e:
        print(f"\n❌ Seed failed: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
