"""
Unit tests for CareerPilot AI Job Matcher & AI Module.
"""

from job_matcher import job_matcher
from utils import extract_skills_from_text


def test_extract_skills():
    sample_text = "Looking for a Senior Python Developer with FastAPI, PyTorch, Docker, and PostgreSQL experience."
    skills = extract_skills_from_text(sample_text)
    
    assert "Python" in skills
    assert "FastAPI" in skills
    assert "PyTorch" in skills
    assert "Docker" in skills
    assert "PostgreSQL" in skills


def test_calculate_match():
    resume_text = "Experienced developer with Python, FastAPI, Docker, and SQL."
    job_desc = "Role requiring Python, FastAPI, PyTorch, Docker, Kubernetes, and AWS."

    result = job_matcher.calculate_match(resume_text, job_desc, "Python Engineer")

    assert "match_percentage" in result
    assert result["match_percentage"] > 0
    assert "Python" in result["matched_skills"]
    assert "Kubernetes" in result["missing_skills"]
    assert len(result["suggestions"]) > 0


def test_generate_cover_letter():
    letter = job_matcher.generate_cover_letter(
        applicant_name="Alex Mercer",
        company_name="TechCorp",
        job_title="Senior Python Architect",
        job_description="Developing LLM services with Python and FastAPI."
    )

    assert "Dear Hiring Manager at TechCorp" in letter
    assert "Senior Python Architect" in letter
    assert "Alex Mercer" in letter
