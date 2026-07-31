"""
CareerPilot AI - Database Management Module
Handles SQLite connection, session management, and sample data seeding.
"""

from datetime import datetime, timedelta
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from config import DATABASE_URL, logger
from models import Base, Job, Application, Resume, Settings


class DatabaseManager:
    """Manages database connection lifecycle, sessions, and table initialization."""

    def __init__(self, db_url=None):
        self.db_url = db_url or DATABASE_URL
        self.engine = create_engine(
            self.db_url, connect_args={"check_same_thread": False}, echo=False
        )
        self.session_factory = sessionmaker(
            bind=self.engine, autocommit=False, autoflush=False
        )
        self.Session = scoped_session(self.session_factory)

    def init_db(self):
        """Create all database tables if they do not exist and apply lightweight column migrations."""
        try:
            Base.metadata.create_all(bind=self.engine)
            
            # Migration check for new city & state columns on existing DB
            with self.engine.connect() as conn:
                from sqlalchemy import inspect, text
                inspector = inspect(self.engine)
                if "jobs" in inspector.get_table_names():
                    columns = [c["name"] for c in inspector.get_columns("jobs")]
                    if "city" not in columns:
                        conn.execute(text("ALTER TABLE jobs ADD COLUMN city VARCHAR(100) DEFAULT 'Remote'"))
                    if "state" not in columns:
                        conn.execute(text("ALTER TABLE jobs ADD COLUMN state VARCHAR(100) DEFAULT 'Remote'"))
                    conn.commit()

            logger.info("Database tables initialized and migrated successfully.")
            self.seed_sample_data()
        except Exception as e:
            logger.error(f"Error initializing database: {e}", exc_info=True)

    def get_session(self):
        """Retrieve a thread-safe database session."""
        return self.Session()

    def seed_sample_data(self):
        """Seed realistic sample data into the database if empty."""
        session = self.get_session()
        try:
            # Check if settings exist
            if session.query(Settings).count() == 0:
                default_settings = Settings(
                    email="candidate@careerpilot.ai",
                    smtp_server="smtp.gmail.com",
                    smtp_port=587,
                    smtp_username="notifications@careerpilot.ai",
                    smtp_password="",
                    voice_enabled=True,
                    voice_wake_word="CareerPilot",
                    openai_api_key="",
                    theme="natural",
                    db_path=str(DATABASE_URL),
                )
                session.add(default_settings)
                logger.info("Seeded default settings.")

            # Check if resumes exist
            if session.query(Resume).count() == 0:
                sample_resume = Resume(
                    version="Senior_Python_AI_Engineer_v2.pdf",
                    filename="Senior_Python_AI_Engineer_v2.pdf",
                    skills="Python, FastAPI, Streamlit, PyTorch, LangChain, OpenAI API, PostgreSQL, Docker, AWS, Scikit-Learn, Pandas, Git, CI/CD, SQL",
                    content_text="""
                    Alex Mercer - Senior Software Engineer & AI Specialist
                    Email: alex.mercer@email.com | Phone: +1-555-0192 | Bhopal, MP / Remote
                    
                    SUMMARY:
                    Senior Full-Stack & AI Engineer with 6+ years of experience designing scalable microservices, automated scraping pipelines, and LLM-powered applications using Python, Streamlit, PyTorch, and Docker.
                    
                    TECHNICAL SKILLS:
                    Languages: Python, JavaScript, TypeScript, SQL, HTML/CSS
                    Frameworks: FastAPI, Flask, Streamlit, PyTorch, React, Django
                    AI & ML: OpenAI API, LangChain, Transformers, Scikit-Learn, Pandas, NumPy
                    Database & Tools: PostgreSQL, SQLite, SQLAlchemy, Redis, Docker, Git, Linux, AWS, Playwright
                    
                    EXPERIENCE:
                    Lead Python Engineer - MP Tech Innovations, Bhopal (2022 - Present)
                    - Built automated data extraction scrapers processing 50,000+ records daily with Playwright & BeautifulSoup.
                    - Developed internal AI analytics dashboard using Streamlit & Plotly, reducing reporting time by 40%.
                    """,
                )
                session.add(sample_resume)
                logger.info("Seeded sample resume.")

            # Check if jobs exist
            if session.query(Job).count() == 0:
                sample_jobs = [
                    {
                        "company": "Bhopal Smart Tech Systems",
                        "title": "Senior Python & AI Architect",
                        "salary": "₹18,00,000 - ₹24,00,000",
                        "location": "Bhopal, Madhya Pradesh",
                        "city": "Bhopal",
                        "state": "Madhya Pradesh",
                        "experience": "Senior Level (5+ yrs)",
                        "description": "Leading tech hub in Bhopal seeking a Senior Python Architect to build AI applications, FastAPI services, and data pipelines.",
                        "url": "https://bhopaltech.example.com/job/101",
                        "date_posted": "2026-07-29",
                        "source": "Local Portal",
                        "skills": "Python, OpenAI API, FastAPI, Streamlit, PostgreSQL, Docker",
                    },
                    {
                        "company": "Indore Software Labs",
                        "title": "Full-Stack Python & Streamlit Engineer",
                        "salary": "₹14,00,000 - ₹18,00,000",
                        "location": "Indore, Madhya Pradesh",
                        "city": "Indore",
                        "state": "Madhya Pradesh",
                        "experience": "Mid-Senior Level",
                        "description": "Develop high-throughput web tools, analytical dashboards, and automation suites using Python and Streamlit in Indore IT Park.",
                        "url": "https://indorelabs.example.com/careers/fs-python",
                        "date_posted": "2026-07-30",
                        "source": "MP Job Portal",
                        "skills": "Python, Streamlit, Pandas, Plotly, SQLite, Git",
                    },
                    {
                        "company": "MP Digital Solutions",
                        "title": "Backend Web Scraping & Playwright Engineer",
                        "salary": "₹12,00,000 - ₹16,00,000",
                        "location": "Bhopal, Madhya Pradesh",
                        "city": "Bhopal",
                        "state": "Madhya Pradesh",
                        "experience": "Mid Level (3+ yrs)",
                        "description": "Build automated web scrapers, browser automation tools, and data pipelines using Python and Playwright in Bhopal.",
                        "url": "https://mpdigital.example.com/jobs/automation",
                        "date_posted": "2026-07-31",
                        "source": "Scraper",
                        "skills": "Python, Playwright, BeautifulSoup, Scraping, Redis",
                    },
                    {
                        "company": "OpenAI Partner Tech",
                        "title": "Lead LLM & Python Developer",
                        "salary": "$160,000 - $190,000",
                        "location": "Remote (India / Global)",
                        "city": "Remote",
                        "state": "Remote",
                        "experience": "Senior Level (5+ yrs)",
                        "description": "Remote LLM development position designing enterprise AI workflows and microservices.",
                        "url": "https://openaipartner.example.com/job/201",
                        "date_posted": "2026-07-28",
                        "source": "RemoteOK",
                        "skills": "Python, OpenAI API, LangChain, PyTorch, Docker",
                    },
                    {
                        "company": "Bangalore Cloud Analytics",
                        "title": "Senior Data & ML Engineer",
                        "salary": "₹25,00,000 - ₹35,00,000",
                        "location": "Bangalore, Karnataka",
                        "city": "Bangalore",
                        "state": "Karnataka",
                        "experience": "Senior (6+ yrs)",
                        "description": "Cloud data architecture and model deployment infrastructure engineer on AWS in Bangalore.",
                        "url": "https://bangalorecloud.example.com/jobs/ml-sr",
                        "date_posted": "2026-07-27",
                        "source": "Indeed",
                        "skills": "Python, AWS, PyTorch, Scikit-Learn, Docker, Kubernetes",
                    },
                ]

                job_objects = []
                for j in sample_jobs:
                    job_obj = Job(
                        company=j["company"],
                        title=j["title"],
                        salary=j["salary"],
                        location=j["location"],
                        city=j["city"],
                        state=j["state"],
                        experience=j["experience"],
                        description=j["description"],
                        url=j["url"],
                        date_posted=j["date_posted"],
                        source=j["source"],
                        skills=j["skills"],
                    )
                    job_objects.append(job_obj)

                session.add_all(job_objects)
                session.commit()
                logger.info(f"Seeded {len(job_objects)} sample jobs.")

                # Seed sample applications linked to jobs
                added_jobs = session.query(Job).all()
                statuses = ["Applied", "Interview", "Offer"]
                notes_list = [
                    "Applied via Bhopal Tech local portal. Initial screening scheduled.",
                    "Passed technical screening. Scheduled 2nd round system design interview.",
                    "Received formal offer letter! Evaluating compensation package.",
                ]

                for i, job_item in enumerate(added_jobs[:3]):
                    status = statuses[i % len(statuses)]
                    interview_date = (
                        datetime.now() + timedelta(days=random.randint(1, 7))
                        if status == "Interview"
                        else None
                    )
                    app = Application(
                        job_id=job_item.id,
                        applied_date=datetime.now()
                        - timedelta(days=random.randint(2, 10)),
                        status=status,
                        interview_date=interview_date,
                        notes=notes_list[i % len(notes_list)],
                    )
                    session.add(app)

                session.commit()
                logger.info("Seeded sample job applications.")

        except Exception as e:
            session.rollback()
            logger.error(f"Error seeding sample data: {e}", exc_info=True)
        finally:
            session.close()


# Singleton database instance helper
db_manager = DatabaseManager()
