"""
CareerPilot AI - Automation Scheduler Module
Runs background cron-style jobs for daily job scraping, email dispatch, resume backups, and log maintenance.
"""

import time
import threading
import shutil
from datetime import datetime
import schedule
from config import LOGS_DIR, RESUMES_DIR, EXPORTS_DIR, logger
from job_scraper import job_scraper
from email_bot import email_bot


class AutomationScheduler:
    """Manages background task schedules and automated routines."""

    def __init__(self):
        self.is_running = False
        self.thread = None

    def daily_scraping_job(self):
        """Task routine for scheduled daily scraping."""
        logger.info("[SCHEDULER] Running automated daily job scraping task...")
        try:
            saved = job_scraper.run_scraping_cycle(is_remote=True)
            logger.info(f"[SCHEDULER] Daily job scraping complete. Saved {saved} new jobs.")
        except Exception as e:
            logger.error(f"[SCHEDULER] Daily job scraping failed: {e}", exc_info=True)

    def daily_email_report_job(self):
        """Task routine for scheduled evening email dispatches."""
        logger.info("[SCHEDULER] Dispatching automated daily email report...")
        try:
            email_bot.send_daily_email()
            logger.info("[SCHEDULER] Daily email report dispatched successfully.")
        except Exception as e:
            logger.error(f"[SCHEDULER] Daily email report dispatch failed: {e}", exc_info=True)

    def daily_resume_backup_job(self):
        """Task routine to create a ZIP backup of all stored resumes."""
        logger.info("[SCHEDULER] Executing daily resume backup...")
        try:
            backup_filename = f"resume_backup_{datetime.now().strftime('%Y%m%d')}"
            archive_path = EXPORTS_DIR / backup_filename
            shutil.make_archive(str(archive_path), 'zip', str(RESUMES_DIR))
            logger.info(f"[SCHEDULER] Resume backup archive created at {archive_path}.zip")
        except Exception as e:
            logger.error(f"[SCHEDULER] Resume backup failed: {e}", exc_info=True)

    def setup_schedules(self):
        """Configure schedule frequencies."""
        schedule.clear()
        # Schedule daily scraping every morning at 08:00
        schedule.every().day.at("08:00").do(self.daily_scraping_job)
        # Schedule daily report email every evening at 18:00
        schedule.every().day.at("18:00").do(self.daily_email_report_job)
        # Schedule daily resume backup at midnight 00:00
        schedule.every().day.at("00:00").do(self.daily_resume_backup_job)
        logger.info("Automation schedules configured successfully.")

    def _loop(self):
        """Internal background loop running pending schedule tasks."""
        while self.is_running:
            schedule.run_pending()
            time.sleep(5)

    def start(self):
        """Start background scheduler thread."""
        if not self.is_running:
            self.setup_schedules()
            self.is_running = True
            self.thread = threading.Thread(target=self._loop, daemon=True)
            self.thread.start()
            logger.info("Background Automation Scheduler started.")

    def stop(self):
        """Stop background scheduler thread."""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=2)
            logger.info("Background Automation Scheduler stopped.")


# Singleton instance helper
automation_scheduler = AutomationScheduler()
