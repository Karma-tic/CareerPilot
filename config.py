"""
CareerPilot AI - Configuration Module
Manages application paths, environment variables, settings, and central logging configuration.
"""

import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Base directory of the CareerPilot project
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env if present
load_dotenv(BASE_DIR / ".env")

# Subdirectories definition
DATABASE_DIR = BASE_DIR / "database"
RESUMES_DIR = BASE_DIR / "resumes"
COVER_LETTERS_DIR = BASE_DIR / "cover_letters"
REPORTS_DIR = BASE_DIR / "reports"
EXPORTS_DIR = BASE_DIR / "exports"
LOGS_DIR = BASE_DIR / "logs"
TEMPLATES_DIR = BASE_DIR / "templates"
ASSETS_DIR = BASE_DIR / "assets"

# Ensure directories exist
for directory in [
    DATABASE_DIR,
    RESUMES_DIR,
    COVER_LETTERS_DIR,
    REPORTS_DIR,
    EXPORTS_DIR,
    LOGS_DIR,
    TEMPLATES_DIR,
    ASSETS_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)

# Default Database Path
DEFAULT_DB_PATH = DATABASE_DIR / "jobs.db"
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH}")

# Logging Setup
LOG_FILE = LOGS_DIR / "careerpilot.log"

logger = logging.getLogger("CareerPilot")
logger.setLevel(logging.INFO)

# Formatter
log_formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(name)s:%(filename)s:%(lineno)d] - %(message)s"
)

# File Handler
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.INFO)

# Console Handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)
console_handler.setLevel(logging.INFO)

# Avoid duplicate handlers if reloaded
if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

class SettingsConfig:
    """Default application settings values."""
    APP_NAME = "CareerPilot AI"
    VERSION = "1.0.0"
    DEFAULT_EMAIL = os.getenv("DEFAULT_EMAIL", "user@example.com")
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    VOICE_WAKE_WORD = os.getenv("VOICE_WAKE_WORD", "CareerPilot")
    THEME = os.getenv("THEME", "dark")
