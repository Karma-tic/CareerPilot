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

## Step-by-Step Guide: How to Automate and Receive Daily Email Reports

Follow these steps to configure real email delivery so you receive daily PDF and CSV summary reports directly in your inbox:

### Step 1: Generate a Gmail App Password (for Gmail Users)
1. Navigate to Google Account Security: `https://myaccount.google.com/security`.
2. Ensure **2-Step Verification** is turned ON.
3. Search for **App Passwords** in the top search bar.
4. Select **Create App Password**, enter `CareerPilot` as the app name, and click **Create**.
5. Copy the generated **16-character passcode** (e.g. `abcd efgh ijkl mnop`).

### Step 2: Configure Credentials in CareerPilot UI
1. Launch the app in your browser at `http://localhost:8501`.
2. Navigate to the **Settings** tab in the sidebar.
3. Fill in your details:
   - **User Email for Reports**: `your_email@gmail.com`
   - **SMTP Server**: `smtp.gmail.com` (or `smtp.office365.com` for Outlook)
   - **SMTP Port**: `587`
   - **SMTP Username**: `your_email@gmail.com`
   - **SMTP Password**: Paste your **16-character App Password** from Step 1.
4. Click **Save Settings**.

### Step 3: Test Email Dispatch & Enable Scheduler
1. Go to the **Overview** tab and click **Dispatch Daily Email Report** to receive a test email immediately in your inbox.
2. Go to the **Voice & Automation** tab and ensure **Background Automation Status** is set to `Running`. CareerPilot will automatically dispatch your PDF report every evening at 18:00.

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
