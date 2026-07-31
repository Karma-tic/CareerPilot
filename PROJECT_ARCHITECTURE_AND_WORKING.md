# CareerPilot — System Architecture & Technical Working Guide

## Overview

**CareerPilot** is a production-grade, modular Python software application designed to automate job searching, application tracking, resume matching, career analytics, voice command interactions, and daily PDF email reporting.

---

## System Architecture & Working Model

```
+-----------------------------------------------------------------------------------+
|                               STREAMLIT DASHBOARD UI                               |
|       (Overview, Job Listings, Application Tracker, Analytics, Matcher, Settings)  |
+-----------------------------------------------------------------------------------+
        |                       |                       |                      |
        v                       v                       v                      v
+---------------+       +---------------+       +---------------+      +---------------+
|  JOB SCRAPER  |       | AI MATCHER    |       |  ANALYTICS    |      | EXPORT ENGINE |
| (Remotive /   |       | (TF-IDF &     |       | (Pandas &     |      | (PDF, CSV,    |
|  RemoteOK/RSS)|       |  OpenAI API)  |       |  Plotly)      |      |  Excel, JSON) |
+---------------+       +---------------+       +---------------+      +---------------+
        |                       |                       |                      |
        +-----------------------+-----------+-----------+----------------------+
                                            |
                                            v
                                +-----------------------+
                                |  SQLAlchemy ORM DB    |
                                |  (SQLite jobs.db)     |
                                +-----------------------+
                                            ^
                                            |
                        +---------------------------------------+
                        |   AUTOMATION SCHEDULER & EMAIL BOT    |
                        |   - Daily Scraping (08:00)            |
                        |   - PDF/CSV Email Dispatch (18:00)   |
                        |   - Resume Zip Backups (00:00)        |
                        +---------------------------------------+
```

---

## Frequently Asked Questions

### 1. Does it work in real time?
**Yes, 100% real-time!**
- **Real-Time Job Scraping**: Clicking **"Run Live Job Scraper"** or entering a search query connects to live remote APIs and RSS job feeds, parses incoming jobs in memory, checks for duplicates, and saves them to the database within seconds.
- **Real-Time UI Updates**: Streamlit reactively refreshes tables, metrics, and Plotly charts as soon as jobs are scraped or application statuses are changed.
- **Real-Time Voice Assistant**: Clicking microphone activation listens to audio commands via `SpeechRecognition`, parses intent, and provides instant audio feedback via `pyttsx3`.

---

### 2. How does the Multi-Layer Location Filter work?
The application implements a 3-Tier Geographic Hierarchy:
- **Layer 1 (City / Local)**: Filters jobs by specific cities (e.g., **Bhopal**, **Indore**, **Bangalore**, **Mumbai**, **Delhi NCR**, **Remote**).
- **Layer 2 (State / Region)**: Groups jobs by state (e.g., **Madhya Pradesh**, **Maharashtra**, **Karnataka**, **Delhi**, **Remote**).
- **Layer 3 (Work Scope)**: Filters by work arrangement (**Remote Only**, **Hybrid**, **On-site**, **All Work Types**).

Selecting a State automatically locks valid Cities; selecting a City automatically locks its State.

---

### 3. How to automate Email Reports & Background Tasks?
CareerPilot includes an embedded background thread managed by `scheduler.py` using Python's `schedule` library:

1. **Daily Auto-Scraping**: Runs every morning at **08:00**.
2. **Daily PDF Email Dispatch**: Runs every evening at **18:00**. Generates a professional PDF report (via ReportLab) and CSV export, attaching both to an HTML email dispatched via SMTP (`smtplib`).
3. **Resume Backup**: Runs at **00:00** creating a ZIP archive of all stored resumes in `exports/`.

#### Setting Up Email Notifications:
1. Open the **Settings** tab in the Streamlit UI.
2. Enter your email address.
3. Configure your SMTP Server (e.g., `smtp.gmail.com`), Port (`587`), Username, and App Password.
4. Click **Save Settings**.

---

## Technology Stack

| Layer | Technologies Used |
|---|---|
| **Programming Language** | Python 3.12+ |
| **User Interface** | Streamlit (Light Cream & Royal Purple Theme), Plotly |
| **Database & ORM** | SQLite, SQLAlchemy 2.0+ |
| **Data Processing & Analytics** | Pandas, NumPy |
| **Scraping & Web Parsing** | Remotive API, RemoteOK API, BeautifulSoup4, Requests, Playwright |
| **AI & Skill Matching** | TF-IDF Cosine Similarity, Regex Taxonomy, OpenAI API |
| **Voice Assistance** | SpeechRecognition, pyttsx3 (Text-To-Speech) |
| **Reporting & Exporters** | ReportLab (PDF), OpenPyXL (Excel), CSV, JSON |
| **Automation & Scheduling** | Schedule (Background Thread Worker), Smtplib |
| **Unit Testing** | Pytest |
