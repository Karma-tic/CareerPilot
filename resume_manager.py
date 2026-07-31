"""
CareerPilot AI - Resume Manager Module
Handles resume uploading, file management, text parsing, and database indexing.
"""

from pathlib import Path
from datetime import datetime
from config import RESUMES_DIR, logger
from database import db_manager
from models import Resume
from utils import extract_skills_from_text


class ResumeManager:
    """Manages uploaded resumes, file system persistence, and DB synchronization."""

    def __init__(self):
        self.resumes_dir = RESUMES_DIR

    def save_resume_file(self, file_bytes: bytes, filename: str) -> Path:
        """Save resume bytes to the resumes directory."""
        clean_filename = filename.replace(" ", "_")
        target_path = self.resumes_dir / clean_filename
        with open(target_path, "wb") as f:
            f.write(file_bytes)
        logger.info(f"Resume saved to disk: {target_path}")
        return target_path

    def parse_resume_content(self, file_path: Path, content_text: str = None) -> str:
        """Parse raw text from resume file or provided string."""
        if content_text:
            return content_text

        # Try basic text reading for txt/md or raw text fallback
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
                return text
        except Exception as e:
            logger.warning(f"Could not read raw text from {file_path}: {e}")
            return f"Resume Content from file: {file_path.name}"

    def upload_and_process_resume(
        self, file_bytes: bytes, filename: str, raw_text: str = None, version: str = None
    ) -> dict:
        """Save resume to disk, extract skills, and persist to database."""
        saved_path = self.save_resume_file(file_bytes, filename)
        parsed_text = self.parse_resume_content(saved_path, raw_text)
        skills_list = extract_skills_from_text(parsed_text)
        skills_str = ", ".join(skills_list) if skills_list else "Python, Engineering, Software"

        version_str = version or f"v{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        session = db_manager.get_session()
        try:
            new_resume = Resume(
                version=version_str,
                filename=filename,
                skills=skills_str,
                content_text=parsed_text,
                uploaded_at=datetime.utcnow(),
            )
            session.add(new_resume)
            session.commit()
            logger.info(f"Resume {filename} indexed in database successfully.")
            return new_resume.to_dict()
        except Exception as e:
            session.rollback()
            logger.error(f"Error persisting resume to DB: {e}", exc_info=True)
            raise e
        finally:
            session.close()

    def get_latest_resume(self) -> dict | None:
        """Get the most recently uploaded resume record."""
        session = db_manager.get_session()
        try:
            resume = session.query(Resume).order_by(Resume.id.desc()).first()
            return resume.to_dict() if resume else None
        finally:
            session.close()

    def get_all_resumes(self) -> list[dict]:
        """Retrieve list of all uploaded resumes."""
        session = db_manager.get_session()
        try:
            resumes = session.query(Resume).order_by(Resume.id.desc()).all()
            return [r.to_dict() for r in resumes]
        finally:
            session.close()


# Singleton instance helper
resume_manager = ResumeManager()
