# CareerPilot

**CareerPilot** is a production-grade, AI-powered Job Search, Application Tracking, and Career Intelligence platform. Built with Python 3.12+, SQLite, SQLAlchemy, Streamlit, Pandas, Plotly, ReportLab, and SpeechRecognition, CareerPilot automates job scraping, resume matching, multi-tier location filtering (Bhopal -> MP -> National/Remote), application pipeline tracking, voice commands, and automated daily PDF email reporting.

---

## Key Features

1. **Multi-Source Job Scraper with Location Hierarchy**
   - Scrapes public tech feeds (Remotive API, RemoteOK API, WeWorkRemotely RSS feeds).
   - Multi-Layer location tagging: **Layer 1: City (Bhopal, Indore, etc.)**, **Layer 2: State (Madhya Pradesh, etc.)**, **Layer 3: Scope (Remote/Hybrid/On-site)**.
   - Saves deduplicated listings directly into SQLite database.

2. **Authentic Light Cream & Royal Purple Streamlit Interface**
   - **Overview**: Executive metrics, recent job table, status count cards, quick actions.
   - **Job Listings**: Locked location filters (City, State, Work Scope, Keywords), 1-click application tracking, AI job description summarization.
   - **Application Tracker**: Pipeline tracking for Applied, Interview, Rejected, Offer, Accepted with note editing and interview calendar reminders.
   - **Analytics & Predictions**: Plotly charts (applications over time, salary distributions, skills frequency, top hiring companies, interview ratios, and predictive skill trends).
   - **AI Resume Matcher**: Upload resume, calculate Match %, analyze missing vs matched skills, receive actionable recommendations, and generate tailored cover letters.
   - **Voice & Automation**: Voice command execution, microphone testing, background scheduler controls.
   - **Settings**: Email, SMTP config, OpenAI API keys, voice wake words, and database settings.

3. **Voice Assistant**
   - Wake Word: `CareerPilot`
   - Voice Commands supported: *"Search Python jobs"*, *"Search remote AI jobs"*, *"Email report"*, *"Read today's summary"*, *"Open resume"*, *"Show dashboard"*.

4. **Automated Email Reporting & Background Scheduler**
   - Daily PDF summary reports (generated with ReportLab) and CSV attachments.
   - Dispatches via SMTP every evening at 18:00 automatically.

5. **Multi-Format Exporters**
   - Export job listings and application tables into **CSV**, **Excel (.xlsx)**, **PDF**, and **JSON**.

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

## Documentation & Architecture

For a detailed explanation of system architecture, real-time data flows, location layering logic, and automation setup, see [PROJECT_ARCHITECTURE_AND_WORKING.md](file:///c:/Users/26050055/Desktop/UI/CareerPilot/PROJECT_ARCHITECTURE_AND_WORKING.md).

---

## Quick Setup & Run Instructions

```bash
# 1. Open project directory
cd CareerPilot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch Streamlit Application
streamlit run app.py
```

---

## Testing

```bash
# Run Pytest unit test suite
python -m pytest -v

# Run full end-to-end integration test
python test_run.py
```
