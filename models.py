"""
CareerPilot AI - SQLAlchemy ORM Models
Defines data structures for Jobs, Applications, Resumes, and Application Settings.
"""

from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    DateTime,
    ForeignKey,
    Boolean,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Job(Base):
    """ORM Model representing a scraped or manually entered Job Listing."""

    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company = Column(String(255), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    salary = Column(String(100), nullable=True, default="Not Disclosed")
    location = Column(String(255), nullable=True, default="Remote")
    city = Column(String(100), nullable=True, default="Remote", index=True)
    state = Column(String(100), nullable=True, default="Remote", index=True)
    experience = Column(String(100), nullable=True, default="Entry / Mid Level")
    description = Column(Text, nullable=True)
    url = Column(String(500), unique=True, nullable=False)
    date_posted = Column(String(100), nullable=True)
    source = Column(String(100), nullable=True, default="Scraper")
    scraped_at = Column(DateTime, default=datetime.utcnow)
    skills = Column(Text, nullable=True)  # Comma-separated list of skills

    # Relationships
    applications = relationship(
        "Application", back_populates="job", cascade="all, delete-orphan"
    )

    def to_dict(self):
        """Convert ORM object to dictionary."""
        return {
            "id": self.id,
            "company": self.company,
            "title": self.title,
            "salary": self.salary,
            "location": self.location,
            "city": self.city or "Remote",
            "state": self.state or "Remote",
            "experience": self.experience,
            "description": self.description,
            "url": self.url,
            "date_posted": self.date_posted,
            "source": self.source,
            "scraped_at": self.scraped_at.strftime("%Y-%m-%d %H:%M:%S")
            if self.scraped_at
            else None,
            "skills": self.skills,
        }


class Application(Base):
    """ORM Model representing a tracked Job Application."""

    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    applied_date = Column(DateTime, default=datetime.utcnow)
    status = Column(
        String(50), nullable=False, default="Applied"
    )  # Applied, Interview, Rejected, Offer, Accepted
    interview_date = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)

    # Relationships
    job = relationship("Job", back_populates="applications")

    def to_dict(self):
        """Convert ORM object to dictionary."""
        return {
            "id": self.id,
            "job_id": self.job_id,
            "company": self.job.company if self.job else "Unknown",
            "title": self.job.title if self.job else "Unknown",
            "applied_date": self.applied_date.strftime("%Y-%m-%d")
            if self.applied_date
            else None,
            "status": self.status,
            "interview_date": self.interview_date.strftime("%Y-%m-%d %H:%M")
            if self.interview_date
            else None,
            "notes": self.notes,
        }


class Resume(Base):
    """ORM Model storing uploaded Resume metadata and parsed content."""

    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    version = Column(String(50), nullable=False, default="v1.0")
    skills = Column(Text, nullable=True)  # Comma separated extracted skills
    filename = Column(String(255), nullable=False)
    content_text = Column(Text, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "version": self.version,
            "skills": self.skills,
            "filename": self.filename,
            "uploaded_at": self.uploaded_at.strftime("%Y-%m-%d %H:%M:%S")
            if self.uploaded_at
            else None,
        }


class Settings(Base):
    """ORM Model storing user preferences, SMTP details, and API configuration."""

    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=True)
    smtp_server = Column(String(255), nullable=True, default="smtp.gmail.com")
    smtp_port = Column(Integer, nullable=True, default=587)
    smtp_username = Column(String(255), nullable=True)
    smtp_password = Column(String(255), nullable=True)
    voice_enabled = Column(Boolean, default=True)
    voice_wake_word = Column(String(100), default="CareerPilot")
    openai_api_key = Column(String(255), nullable=True)
    theme = Column(String(50), default="natural")
    db_path = Column(String(500), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "smtp_server": self.smtp_server,
            "smtp_port": self.smtp_port,
            "smtp_username": self.smtp_username,
            "smtp_password": self.smtp_password,
            "voice_enabled": self.voice_enabled,
            "voice_wake_word": self.voice_wake_word,
            "openai_api_key": self.openai_api_key,
            "theme": self.theme,
            "db_path": self.db_path,
        }
