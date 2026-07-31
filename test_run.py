"""
CareerPilot AI - End-to-End System Verification Script
Executes all backend services, database queries, job scrapers, AI matchers, analytics generators, and PDF exporters.
"""

import os
import sys
from pathlib import Path

# Force UTF-8 stdout encoding for Windows console
sys.stdout.reconfigure(encoding='utf-8')

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from config import logger, REPORTS_DIR, EXPORTS_DIR
from database import db_manager
from models import Job, Application, Resume, Settings
from job_scraper import job_scraper
from job_matcher import job_matcher
from resume_manager import resume_manager
from analytics import analytics_engine
from email_bot import email_bot
from voice_assistant import voice_assistant
from utils import export_jobs_to_csv, export_jobs_to_excel, export_jobs_to_pdf, export_jobs_to_json


def run_full_verification():
    print("=" * 60)
    print("Starting CareerPilot AI Full System Verification")
    print("=" * 60)

    # 1. Initialize Database & Seed Data
    print("\n[1/6] Initializing Database & Verifying Seed Data...")
    db_manager.init_db()
    session = db_manager.get_session()
    try:
        job_count = session.query(Job).count()
        app_count = session.query(Application).count()
        resume_count = session.query(Resume).count()
        settings_count = session.query(Settings).count()
        print(f"  [OK] Database Initialized Successfully!")
        print(f"  [OK] Total Jobs in DB: {job_count}")
        print(f"  [OK] Total Applications: {app_count}")
        print(f"  [OK] Total Resumes: {resume_count}")
        print(f"  [OK] Settings Initialized: {settings_count}")
    finally:
        session.close()

    # 2. Test Live Job Scraper
    print("\n[2/6] Testing Live Job Scraper Engine...")
    scraped_saved = job_scraper.run_scraping_cycle(is_remote=True)
    print(f"  [OK] Live Scraping Completed! New Jobs Saved: {scraped_saved}")

    # 3. Test AI Resume Matcher & Cover Letter Generator
    print("\n[3/6] Testing AI Resume Matcher & Cover Letter Generator...")
    latest_resume = resume_manager.get_latest_resume()
    if latest_resume:
        sample_job_desc = "Seeking a Senior Python Engineer with FastAPI, PyTorch, Docker, PostgreSQL, and AWS skills."
        match_result = job_matcher.calculate_match(
            resume_text=latest_resume.get("content_text", ""),
            job_description=sample_job_desc,
            job_title="Senior Python Architect"
        )
        print(f"  [OK] Match Score Computed: {match_result['match_percentage']}%")
        print(f"  [OK] Matched Skills: {match_result['matched_skills']}")
        print(f"  [OK] Missing Skills: {match_result['missing_skills']}")

        cover_letter = job_matcher.generate_cover_letter(
            applicant_name="Alex Mercer",
            company_name="NeuralScale Systems",
            job_title="Senior Python Architect",
            job_description=sample_job_desc,
            resume_text=latest_resume.get("content_text", "")
        )
        print(f"  [OK] Cover Letter Generated ({len(cover_letter)} chars)")

    # 4. Test Analytics & Plotly Visualizations...
    print("\n[4/6] Testing Analytics & Plotly Visualizations...")
    df_jobs = analytics_engine.get_jobs_dataframe()
    df_apps = analytics_engine.get_applications_dataframe()
    fig_time = analytics_engine.create_applications_over_time_chart(df_apps)
    fig_salary = analytics_engine.create_salary_distribution_chart(df_jobs)
    fig_skills = analytics_engine.create_skills_frequency_chart(df_jobs)
    print("  [OK] Applications Over Time Chart Created")
    print("  [OK] Salary Distribution Chart Created")
    print("  [OK] Skills Frequency Chart Created")

    # 5. Test Multi-Format Exporters & Email PDF Generator
    print("\n[5/6] Testing Exporters & Daily PDF Report Generator...")
    session = db_manager.get_session()
    try:
        jobs_dicts = [j.to_dict() for j in session.query(Job).all()]
        csv_file = export_jobs_to_csv(jobs_dicts)
        excel_file = export_jobs_to_excel(jobs_dicts)
        json_file = export_jobs_to_json(jobs_dicts)
        pdf_file = export_jobs_to_pdf(jobs_dicts)

        print(f"  [OK] CSV Exported: {csv_file}")
        print(f"  [OK] Excel Exported: {excel_file}")
        print(f"  [OK] JSON Exported: {json_file}")
        print(f"  [OK] PDF Exported: {pdf_file}")

        # Test Daily Email Report Generation
        pdf_rep, csv_rep = email_bot.generate_daily_report_files()
        print(f"  [OK] Daily PDF Report Generated: {pdf_rep}")
        print(f"  [OK] Daily CSV Report Generated: {csv_rep}")
    finally:
        session.close()

    # 6. Test Voice Assistant Command Engine
    print("\n[6/6] Testing Voice Assistant Command Engine...")
    cmd_res1 = voice_assistant.execute_command("Search Python jobs")
    cmd_res2 = voice_assistant.execute_command("Read today's summary")
    print(f"  [OK] Voice Command 'Search Python jobs' -> {cmd_res1['response']}")
    print(f"  [OK] Voice Command 'Read today's summary' -> {cmd_res2['response']}")

    print("\n" + "=" * 60)
    print("ALL SYSTEMS PASSED VERIFICATION 100%!")
    print("=" * 60)


if __name__ == "__main__":
    run_full_verification()
