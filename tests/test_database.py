"""
Unit tests for CareerPilot AI Database Manager & ORM Models.
"""

import pytest
from database import DatabaseManager
from models import Job, Application, Resume, Settings


@pytest.fixture
def temp_db_manager(tmp_path):
    db_file = tmp_path / "test_jobs.db"
    db_url = f"sqlite:///{db_file}"
    manager = DatabaseManager(db_url=db_url)
    manager.init_db()
    return manager


def test_db_initialization_and_seeding(temp_db_manager):
    session = temp_db_manager.get_session()
    try:
        settings_count = session.query(Settings).count()
        jobs_count = session.query(Job).count()
        apps_count = session.query(Application).count()
        resume_count = session.query(Resume).count()

        assert settings_count >= 1
        assert jobs_count >= 5
        assert apps_count >= 3
        assert resume_count >= 1
    finally:
        session.close()


def test_add_job_and_application(temp_db_manager):
    session = temp_db_manager.get_session()
    try:
        new_job = Job(
            company="Test Inc",
            title="Python Test Engineer",
            salary="$120,000",
            location="Remote",
            url="https://example.com/test-job-1",
            skills="Python, Pytest, Git",
        )
        session.add(new_job)
        session.commit()

        assert new_job.id is not None

        new_app = Application(
            job_id=new_job.id,
            status="Applied",
            notes="Testing application creation.",
        )
        session.add(new_app)
        session.commit()

        assert new_app.id is not None
        assert new_app.job.title == "Python Test Engineer"
    finally:
        session.close()
