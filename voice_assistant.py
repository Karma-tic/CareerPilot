"""
CareerPilot AI - Voice Assistant Module
Listens for wake word 'CareerPilot', processes voice commands, and responds via pyttsx3 TTS.
"""

import threading
import speech_recognition as sr
import pyttsx3
from config import logger
from database import db_manager
from models import Job, Application


class VoiceAssistant:
    """Speech recognition and text-to-speech voice interaction engine."""

    def __init__(self, wake_word: str = "CareerPilot"):
        self.wake_word = wake_word.lower()
        self.recognizer = sr.Recognizer()
        self.tts_lock = threading.Lock()

    def speak(self, text: str):
        """Speak out text using pyttsx3 engine safely in a background thread."""
        def run_tts():
            with self.tts_lock:
                try:
                    engine = pyttsx3.init()
                    engine.setProperty("rate", 175)
                    engine.say(text)
                    engine.runAndWait()
                    engine.stop()
                except Exception as e:
                    logger.warning(f"Voice Assistant TTS audio output unavailable: {e}")

        tts_thread = threading.Thread(target=run_tts, daemon=True)
        tts_thread.start()

    def listen_command(self) -> str | None:
        """Listen to microphone input and convert speech to text."""
        try:
            with sr.Microphone() as source:
                logger.info("Voice Assistant listening on microphone...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=7)
                command_text = self.recognizer.recognize_google(audio)
                logger.info(f"Recognized voice speech: '{command_text}'")
                return command_text
        except sr.WaitTimeoutError:
            logger.info("Voice listening timed out (no speech detected).")
            return None
        except Exception as e:
            logger.warning(f"Microphone input or SpeechRecognition unavailable: {e}")
            return None

    def execute_command(self, command_str: str) -> dict:
        """Parse voice or text command string and execute corresponding platform action."""
        if not command_str:
            return {"status": "error", "response": "No command received."}

        cmd_lower = command_str.lower()
        session = db_manager.get_session()

        try:
            if "search python" in cmd_lower or "python jobs" in cmd_lower:
                count = session.query(Job).filter(Job.title.ilike("%Python%")).count()
                reply = f"Found {count} Python jobs in your database. Opening job listings view."
                self.speak(reply)
                return {"status": "success", "action": "navigate", "page": "Job Listings", "filter": "Python", "response": reply}

            elif "search remote ai" in cmd_lower or "ai jobs" in cmd_lower:
                count = session.query(Job).filter(Job.title.ilike("%AI%") | Job.description.ilike("%AI%")).count()
                reply = f"Found {count} remote AI jobs matching your search criteria."
                self.speak(reply)
                return {"status": "success", "action": "navigate", "page": "Job Listings", "filter": "AI", "response": reply}

            elif "email report" in cmd_lower or "send report" in cmd_lower:
                from email_bot import email_bot
                email_bot.send_daily_email()
                reply = "Daily CareerPilot report PDF and CSV has been generated and queued for email dispatch."
                self.speak(reply)
                return {"status": "success", "action": "email", "response": reply}

            elif "today's summary" in cmd_lower or "summary" in cmd_lower or "read summary" in cmd_lower:
                jobs_count = session.query(Job).count()
                apps_count = session.query(Application).count()
                interviews = session.query(Application).filter(Application.status == "Interview").count()
                reply = f"Today's summary: You have {jobs_count} total scraped jobs, {apps_count} active applications, and {interviews} scheduled interviews."
                self.speak(reply)
                return {"status": "success", "action": "summary", "response": reply}

            elif "open resume" in cmd_lower or "show resume" in cmd_lower:
                reply = "Opening AI Resume Matcher and resume manager."
                self.speak(reply)
                return {"status": "success", "action": "navigate", "page": "Resume Match", "response": reply}

            elif "show dashboard" in cmd_lower or "overview" in cmd_lower:
                reply = "Navigating to main overview dashboard."
                self.speak(reply)
                return {"status": "success", "action": "navigate", "page": "Overview", "response": reply}

            else:
                reply = f"Command '{command_str}' recognized, but not mapped to a specific action."
                self.speak(reply)
                return {"status": "info", "response": reply}

        finally:
            session.close()


# Singleton instance helper
voice_assistant = VoiceAssistant()
