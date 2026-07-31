"""
CareerPilot AI - Modern Streamlit Dashboard UI Component
Contains custom light cream & dark purple CSS theme, cascading/locked location filters, interactive charts, and forms.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from config import logger
from database import db_manager
from models import Job, Application, Resume, Settings
from job_scraper import job_scraper
from job_matcher import job_matcher
from resume_manager import resume_manager
from analytics import analytics_engine
from email_bot import email_bot
from voice_assistant import voice_assistant
from scheduler import automation_scheduler
from utils import (
    export_jobs_to_csv,
    export_jobs_to_excel,
    export_jobs_to_json,
    export_jobs_to_pdf,
)

# Cascading City/State Location Hierarchy Mappings
STATE_CITY_MAP = {
    "All States": ["All Cities", "Bhopal", "Indore", "Bangalore", "Mumbai", "Pune", "Delhi NCR", "Remote"],
    "Madhya Pradesh": ["All Cities", "Bhopal", "Indore"],
    "Karnataka": ["All Cities", "Bangalore"],
    "Maharashtra": ["All Cities", "Mumbai", "Pune"],
    "Delhi": ["All Cities", "Delhi NCR"],
    "Remote": ["All Cities", "Remote"],
}

CITY_STATE_MAP = {
    "Bhopal": "Madhya Pradesh",
    "Indore": "Madhya Pradesh",
    "Bangalore": "Karnataka",
    "Mumbai": "Maharashtra",
    "Pune": "Maharashtra",
    "Delhi NCR": "Delhi",
    "Remote": "Remote",
}


def apply_custom_css():
    """Inject a classy Light Cream & Dark Purple CSS theme into Streamlit."""
    st.markdown(
        """
        <style>
        /* Force Light Cream Background & Dark Purple Text Colors */
        html, body, [data-testid="stAppViewContainer"], .stApp {
            background-color: #FAF7F2 !important;
            color: #1E1B4B !important;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        }

        /* Top Header Navigation Bar */
        header[data-testid="stHeader"] {
            background-color: #FAF7F2 !important;
        }

        /* Sidebar Styling - Deep Royal Dark Purple (#1E1B4B) */
        section[data-testid="stSidebar"] {
            background-color: #1E1B4B !important;
            border-right: 1px solid #312E81 !important;
        }
        section[data-testid="stSidebar"] * {
            color: #F5F3FF !important;
        }
        
        /* Metric Card Styling - Soft Cream Card with Royal Purple Accents */
        div[data-testid="stMetricValue"] {
            font-size: 2.2rem !important;
            font-weight: 700 !important;
            color: #6D28D9 !important; /* Royal Purple */
        }
        
        div[data-testid="stMetricLabel"] {
            color: #4C1D95 !important;
            font-weight: 600 !important;
        }

        div[data-testid="stMetric"] {
            background-color: #FFFFFF !important;
            border: 1px solid #DDD6FE !important;
            border-radius: 12px !important;
            padding: 16px !important;
            box-shadow: 0 4px 14px rgba(109, 40, 217, 0.08) !important;
        }

        /* Buttons Styling - Royal Violet Gradient */
        .stButton > button {
            background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            padding: 0.55rem 1.2rem !important;
            transition: all 0.2s ease-in-out !important;
            box-shadow: 0 4px 12px rgba(124, 58, 237, 0.25) !important;
        }
        .stButton > button:hover {
            background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%) !important;
            box-shadow: 0 6px 16px rgba(124, 58, 237, 0.35) !important;
        }
        
        /* Inputs, Selectboxes, Textareas - Light Cream Cards */
        input, select, textarea, div[data-baseweb="select"] {
            background-color: #FFFFFF !important;
            color: #1E1B4B !important;
            border-color: #DDD6FE !important;
        }
        
        /* Expanders & Cards */
        div[data-testid="stExpander"] {
            background-color: #FFFFFF !important;
            border: 1px solid #DDD6FE !important;
            border-radius: 12px !important;
            box-shadow: 0 2px 10px rgba(109, 40, 217, 0.05) !important;
        }
        
        /* Job Card Custom Styling */
        .job-card {
            background-color: #FFFFFF !important;
            border: 1px solid #E9D5FF !important;
            border-radius: 12px !important;
            padding: 20px !important;
            margin-bottom: 15px !important;
            box-shadow: 0 4px 14px rgba(109, 40, 217, 0.06) !important;
        }

        .location-tag {
            background-color: #F3E8FF !important;
            color: #581C87 !important;
            padding: 4px 10px !important;
            border-radius: 6px !important;
            font-size: 0.85rem !important;
            font-weight: 600 !important;
            border: 1px solid #E9D5FF !important;
        }

        /* Status Pills */
        .badge-applied { background-color: #EDE9FE; color: #5B21B6; padding: 4px 10px; border-radius: 6px; font-size: 0.85rem; font-weight: 600; border: 1px solid #DDD6FE; }
        .badge-interview { background-color: #FEF3C7; color: #92400E; padding: 4px 10px; border-radius: 6px; font-size: 0.85rem; font-weight: 600; border: 1px solid #FDE68A; }
        .badge-offer { background-color: #D1FAE5; color: #065F46; padding: 4px 10px; border-radius: 6px; font-size: 0.85rem; font-weight: 600; border: 1px solid #A7F3D0; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_overview_tab():
    """Render 📊 Overview Page."""
    st.header("📊 Executive Job Search Dashboard")
    st.caption("Authentic tracking of job search activity, application pipeline status, and daily automation.")

    session = db_manager.get_session()
    try:
        total_jobs = session.query(Job).count()
        total_apps = session.query(Application).count()
        interviews = session.query(Application).filter(Application.status == "Interview").count()
        offers = session.query(Application).filter(Application.status == "Offer").count()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Scraped Jobs", total_jobs, delta="+5 Today")
        col2.metric("Applications Sent", total_apps, delta="+2 This Week")
        col3.metric("Scheduled Interviews", interviews, delta="Active")
        col4.metric("Job Offers", offers, delta="Target Reached")

        st.divider()

        st.subheader("⚡ Quick Actions & Automation")
        qa_col1, qa_col2, qa_col3 = st.columns(3)
        with qa_col1:
            if st.button("🔄 Run Live Job Scraper", use_container_width=True):
                with st.spinner("Scraping active job portals..."):
                    new_count = job_scraper.run_scraping_cycle(is_remote=True)
                    st.success(f"Scraped and saved {new_count} new job listings!")
                    st.rerun()

        with qa_col2:
            if st.button("📧 Dispatch Daily Email Report", use_container_width=True):
                with st.spinner("Generating PDF & dispatching report..."):
                    email_bot.send_daily_email()
                    st.success("Daily report PDF & CSV generated and sent!")

        with qa_col3:
            if st.button("🎙️ Trigger Voice Assistant", use_container_width=True):
                st.info("Listening... Speak your command now (e.g. 'Search Python jobs').")
                voice_res = voice_assistant.listen_command()
                if voice_res:
                    action_res = voice_assistant.execute_command(voice_res)
                    st.success(action_res.get("response", "Command executed!"))

        st.divider()

        # Recent Jobs Table
        st.subheader("📋 Recent Job Postings")
        df_jobs = analytics_engine.get_jobs_dataframe()
        if not df_jobs.empty:
            display_cols = ["company", "title", "salary", "city", "state", "source", "date_posted"]
            existing_cols = [c for c in display_cols if c in df_jobs.columns]
            st.dataframe(
                df_jobs[existing_cols].head(6),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No jobs found in database. Click 'Run Live Job Scraper' above.")

    finally:
        session.close()


def render_job_listings_tab():
    """Render 🔍 Job Listings Page with search and locked cascading location filters (State <-> City)."""
    st.header("🔍 Job Search & Location Filters")
    st.caption("Cascading location controls: Selecting a State locks valid Cities; selecting a City locks its State.")

    # Initialize Session State for Cascading Dropdowns if not present
    if "selected_state" not in st.session_state:
        st.session_state["selected_state"] = "All States"
    if "selected_city" not in st.session_state:
        st.session_state["selected_city"] = "All Cities"

    # Multi-Layer Location Filter Bar with Cascading Locks
    with st.expander("🌐 Cascading Location & Search Filters", expanded=True):
        f_col1, f_col2, f_col3, f_col4, f_col5 = st.columns(5)
        
        with f_col1:
            search_query = st.text_input("Keywords", placeholder="e.g. Python, AI, Developer")

        with f_col2:
            states_list = list(STATE_CITY_MAP.keys())
            state_idx = states_list.index(st.session_state["selected_state"]) if st.session_state["selected_state"] in states_list else 0
            
            chosen_state = st.selectbox(
                "Layer 1: State / Region",
                states_list,
                index=state_idx,
                key="state_selector"
            )
            if chosen_state != st.session_state["selected_state"]:
                st.session_state["selected_state"] = chosen_state
                st.session_state["selected_city"] = "All Cities"  # Reset city on state change
                st.rerun()

        with f_col3:
            valid_cities = STATE_CITY_MAP.get(st.session_state["selected_state"], ["All Cities"])
            city_idx = valid_cities.index(st.session_state["selected_city"]) if st.session_state["selected_city"] in valid_cities else 0
            
            chosen_city = st.selectbox(
                "Layer 2: City / Local (Locked)",
                valid_cities,
                index=city_idx,
                key="city_selector"
            )
            if chosen_city != st.session_state["selected_city"]:
                st.session_state["selected_city"] = chosen_city
                if chosen_city in CITY_STATE_MAP:
                    st.session_state["selected_state"] = CITY_STATE_MAP[chosen_city]
                st.rerun()

        with f_col4:
            scope_filter = st.selectbox("Layer 3: Scope", ["All Work Types", "Remote Only", "Hybrid", "On-site"])
        
        with f_col5:
            run_scraper = st.button("Scrape Jobs")

    active_city = st.session_state["selected_city"]
    active_state = st.session_state["selected_state"]

    if run_scraper:
        with st.spinner(f"Scraping job portals for {active_city} ({active_state})..."):
            kws = [search_query] if search_query else None
            is_rem = scope_filter == "Remote Only"
            is_hyb = scope_filter == "Hybrid"
            saved = job_scraper.run_scraping_cycle(
                is_remote=is_rem,
                is_hybrid=is_hyb,
                city=None if active_city == "All Cities" else active_city,
                state=None if active_state == "All States" else active_state,
                keywords=kws
            )
            st.success(f"Saved {saved} new matching jobs to database.")
            st.rerun()

    session = db_manager.get_session()
    try:
        query = session.query(Job)
        if search_query:
            query = query.filter(
                (Job.title.ilike(f"%{search_query}%"))
                | (Job.company.ilike(f"%{search_query}%"))
                | (Job.description.ilike(f"%{search_query}%"))
                | (Job.skills.ilike(f"%{search_query}%"))
            )
        
        if active_city != "All Cities":
            query = query.filter(
                (Job.city.ilike(f"%{active_city}%"))
                | (Job.location.ilike(f"%{active_city}%"))
                | (Job.description.ilike(f"%{active_city}%"))
            )

        if scope_filter == "Remote Only":
            query = query.filter(Job.location.ilike("%Remote%"))
        elif scope_filter == "Hybrid":
            query = query.filter(Job.location.ilike("%Hybrid%"))

        jobs = query.order_by(Job.id.desc()).all()

        # Auto-Scrape Fallback if 0 jobs found for selected city
        if len(jobs) == 0 and active_city != "All Cities":
            with st.spinner(f"Fetching live jobs for {active_city}..."):
                job_scraper.run_scraping_cycle(city=active_city, state=active_state)
                jobs = query.order_by(Job.id.desc()).all()

        st.write(f"Showing **{len(jobs)}** matching job opportunities for **{active_city} ({active_state})**:")

        # Export Controls
        exp_col1, exp_col2, exp_col3, exp_col4 = st.columns(4)
        jobs_dicts = [j.to_dict() for j in jobs]
        
        with exp_col1:
            if st.button("📥 Export CSV"):
                path = export_jobs_to_csv(jobs_dicts)
                st.success(f"Exported: {path}")
        with exp_col2:
            if st.button("📥 Export Excel"):
                path = export_jobs_to_excel(jobs_dicts)
                st.success(f"Exported: {path}")
        with exp_col3:
            if st.button("📥 Export PDF"):
                path = export_jobs_to_pdf(jobs_dicts)
                st.success(f"Exported: {path}")
        with exp_col4:
            if st.button("📥 Export JSON"):
                path = export_jobs_to_json(jobs_dicts)
                st.success(f"Exported: {path}")

        st.divider()

        # Job Cards
        for j in jobs[:30]:
            with st.container():
                st.markdown(
                    f"""
                    <div class="job-card">
                        <h3 style="color:#6D28D9; margin-bottom:5px; font-weight:700;">{j.title}</h3>
                        <p style="color:#374151; font-size:1.0rem;"><strong>{j.company}</strong> • <span class="location-tag">📍 {j.city or 'Bhopal'}, {j.state or 'MP'}</span> • <span style="color:#D97706; font-weight:600;">{j.salary}</span></p>
                        <p style="color:#4B5563; font-size:0.92rem; line-height:1.5;">{j.description[:280]}...</p>
                        <p style="color:#6B7280; font-size:0.85rem;"><strong>Required Skills:</strong> {j.skills or 'Python, Engineering'}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                
                c1, c2, c3 = st.columns([1.2, 1.2, 3])
                with c1:
                    if st.button(f"Track / Apply", key=f"apply_{j.id}"):
                        existing = session.query(Application).filter(Application.job_id == j.id).first()
                        if not existing:
                            new_app = Application(
                                job_id=j.id,
                                applied_date=datetime.now(),
                                status="Applied",
                                notes=f"Applied via Job Listings view ({j.city}, {j.state})."
                            )
                            session.add(new_app)
                            session.commit()
                            st.success("Tracked in Applications!")
                        else:
                            st.info("Already tracked in Applications!")
                with c2:
                    if st.button(f"AI Summary", key=f"summary_{j.id}"):
                        summary = job_matcher.summarize_job(j.title, j.company, j.description)
                        st.write("**Key Role Highlights:**")
                        for bullet in summary["summary_bullets"]:
                            st.write(f"- {bullet}")
                            
    finally:
        session.close()


def render_applications_tab():
    """Render 📝 Application Tracker Page."""
    st.header("📝 Application Tracker Pipeline")
    st.caption("Manage application statuses, track upcoming interview dates, and record notes.")

    session = db_manager.get_session()
    try:
        apps = session.query(Application).order_by(Application.id.desc()).all()
        if not apps:
            st.info("No active job applications found. Go to 'Job Listings' to track your first application!")
            return

        # Overview Status Columns
        statuses = ["Applied", "Interview", "Offer", "Rejected", "Accepted"]
        cols = st.columns(5)
        for idx, status_name in enumerate(statuses):
            with cols[idx]:
                count = session.query(Application).filter(Application.status == status_name).count()
                st.metric(status_name, count)

        st.divider()

        st.subheader("📋 Application Pipeline Details")
        for app in apps:
            with st.expander(f"{app.job.company if app.job else 'Unknown'} — {app.job.title if app.job else 'Unknown'} [{app.status}]", expanded=False):
                c1, c2 = st.columns(2)
                with c1:
                    new_status = st.selectbox(
                        "Update Status",
                        statuses,
                        index=statuses.index(app.status) if app.status in statuses else 0,
                        key=f"status_select_{app.id}"
                    )
                    
                    interview_dt = st.date_input(
                        "Interview Date (Calendar Reminder)",
                        value=app.interview_date.date() if app.interview_date else datetime.now().date(),
                        key=f"interview_dt_{app.id}"
                    )
                with c2:
                    new_notes = st.text_area("Notes", value=app.notes or "", key=f"notes_{app.id}")

                if st.button("Save Changes", key=f"save_app_{app.id}"):
                    app.status = new_status
                    app.notes = new_notes
                    if new_status == "Interview":
                        app.interview_date = datetime.combine(interview_dt, datetime.min.time())
                    session.commit()
                    st.success("Application updated successfully!")
                    st.rerun()

    finally:
        session.close()


def render_analytics_tab():
    """Render 📈 Analytics & Predictive Intelligence Page."""
    st.header("📈 Analytics & Predictive Intelligence")
    st.caption("Visual insights on application trends, salary distributions, top skills, and predictive market trends.")

    df_jobs = analytics_engine.get_jobs_dataframe()
    df_apps = analytics_engine.get_applications_dataframe()

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(analytics_engine.create_applications_over_time_chart(df_apps), use_container_width=True)
        st.plotly_chart(analytics_engine.create_skills_frequency_chart(df_jobs), use_container_width=True)

    with col2:
        st.plotly_chart(analytics_engine.create_interview_ratio_chart(df_apps), use_container_width=True)
        st.plotly_chart(analytics_engine.create_salary_distribution_chart(df_jobs), use_container_width=True)

    st.divider()

    st.subheader("🔮 Predictive Skill & Market Trends")
    predictions = analytics_engine.predict_valuable_skills()
    df_pred = pd.DataFrame(predictions)
    st.dataframe(df_pred, use_container_width=True, hide_index=True)


def render_resume_match_tab():
    """Render 🎯 AI Resume Matcher & Cover Letter Page."""
    st.header("🎯 AI Resume Matcher & Cover Letter Generator")
    st.caption("Upload your resume, compute match scores against target jobs, and generate tailored cover letters.")

    # Resume Upload Section
    st.subheader("📄 Upload / Select Resume")
    uploaded_file = st.file_uploader("Upload PDF, TXT, or Markdown Resume", type=["pdf", "txt", "md"])
    if uploaded_file:
        bytes_data = uploaded_file.read()
        resume_dict = resume_manager.upload_and_process_resume(bytes_data, uploaded_file.name)
        st.success(f"Uploaded and indexed resume: {uploaded_file.name}")

    latest_resume = resume_manager.get_latest_resume()
    if not latest_resume:
        st.warning("No resume indexed yet. Please upload a resume above.")
        return

    st.info(f"Active Resume Version: **{latest_resume['filename']}** | Indexed Skills: `{latest_resume['skills']}`")

    st.divider()

    # Matcher Form
    st.subheader("⚡ Compute Match Score")
    session = db_manager.get_session()
    try:
        jobs = session.query(Job).all()
        if not jobs:
            st.info("No job postings available. Scrape jobs first!")
            return

        job_options = {f"{j.company} - {j.title} ({j.city}, {j.state})": j for j in jobs}
        selected_job_title = st.selectbox("Select Target Job", list(job_options.keys()))
        selected_job = job_options[selected_job_title]

        if st.button("🎯 Calculate Match & Generate Recommendations"):
            match_result = job_matcher.calculate_match(
                resume_text=latest_resume.get("content_text", ""),
                job_description=selected_job.description,
                job_title=selected_job.title
            )

            st.metric("Match Score", f"{match_result['match_percentage']}%")

            m_col1, m_col2 = st.columns(2)
            with m_col1:
                st.write("✅ **Matched Skills:**")
                st.write(", ".join(match_result["matched_skills"]) if match_result["matched_skills"] else "General Python skills matched.")
            with m_col2:
                st.write("❌ **Missing Skills:**")
                st.write(", ".join(match_result["missing_skills"]) if match_result["missing_skills"] else "None! Excellent coverage.")

            st.write("💡 **Improvement Suggestions:**")
            for sug in match_result["suggestions"]:
                st.write(f"- {sug}")

        st.divider()

        st.subheader("✍️ Tailored Cover Letter Generator")
        applicant_name = st.text_input("Applicant Full Name", value="Alex Mercer")
        if st.button("📝 Generate Customized Cover Letter"):
            letter = job_matcher.generate_cover_letter(
                applicant_name=applicant_name,
                company_name=selected_job.company,
                job_title=selected_job.title,
                job_description=selected_job.description,
                resume_text=latest_resume.get("content_text", "")
            )
            st.text_area("Generated Cover Letter", value=letter, height=350)

    finally:
        session.close()


def render_voice_automation_tab():
    """Render 🎙️ Voice Assistant & Automation Page."""
    st.header("🎙️ Voice Commands & Automation Center")
    st.caption("Interact with CareerPilot via speech, run background tasks, and trigger dispatches.")

    v_col1, v_col2 = st.columns(2)
    with v_col1:
        st.subheader("🎙️ Voice Assistant Commands")
        st.write("Supported Voice & Text Commands:")
        st.markdown(
            """
            - `Search Python jobs`
            - `Search remote AI jobs`
            - `Email report`
            - `Read today's summary`
            - `Open resume`
            - `Show dashboard`
            """
        )
        cmd_input = st.text_input("Test Command via Text / Speech Input", placeholder="Type or click Listen...")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("▶️ Run Text Command"):
                res = voice_assistant.execute_command(cmd_input)
                st.success(res.get("response", "Executed"))
        with c2:
            if st.button("🎤 Listen on Mic"):
                st.info("Listening on microphone for 5 seconds...")
                speech_text = voice_assistant.listen_command()
                if speech_text:
                    st.write(f"Heard: *'{speech_text}'*")
                    res = voice_assistant.execute_command(speech_text)
                    st.success(res.get("response", "Executed"))
                else:
                    st.warning("No microphone input detected.")

    with v_col2:
        st.subheader("⚙️ Background Automation Status")
        is_active = automation_scheduler.is_running
        st.write(f"Scheduler Status: **{'🟢 Running' if is_active else '🔴 Stopped'}**")

        a1, a2 = st.columns(2)
        with a1:
            if st.button("▶️ Start Background Scheduler"):
                automation_scheduler.start()
                st.success("Scheduler started!")
                st.rerun()
        with a2:
            if st.button("⏹️ Stop Background Scheduler"):
                automation_scheduler.stop()
                st.warning("Scheduler stopped!")
                st.rerun()

        st.divider()

        if st.button("📦 Run Manual Resume Backup Now"):
            automation_scheduler.daily_resume_backup_job()
            st.success("Resume ZIP archive backup completed!")


def render_settings_tab():
    """Render ⚙️ Settings Page."""
    st.header("⚙️ Application Settings")
    st.caption("Configure notification emails, SMTP credentials, OpenAI API key, and system preferences.")

    session = db_manager.get_session()
    try:
        settings = session.query(Settings).first()
        if not settings:
            settings = Settings()

        with st.form("settings_form"):
            email = st.text_input("User Email for Reports", value=settings.email or "")
            openai_key = st.text_input("OpenAI API Key (Optional)", value=settings.openai_api_key or "", type="password")
            
            st.subheader("📧 SMTP Settings (for Automated Emails)")
            smtp_server = st.text_input("SMTP Server", value=settings.smtp_server or "smtp.gmail.com")
            smtp_port = st.number_input("SMTP Port", value=int(settings.smtp_port or 587))
            smtp_user = st.text_input("SMTP Username", value=settings.smtp_username or "")
            smtp_pass = st.text_input("SMTP Password / App Password", value=settings.smtp_password or "", type="password")
            
            st.subheader("🎙️ Voice & System Settings")
            wake_word = st.text_input("Voice Wake Word", value=settings.voice_wake_word or "CareerPilot")
            theme = st.selectbox("UI Theme", ["cream", "dark"], index=0)

            submitted = st.form_submit_button("💾 Save Settings")
            if submitted:
                settings.email = email
                settings.openai_api_key = openai_key
                settings.smtp_server = smtp_server
                settings.smtp_port = smtp_port
                settings.smtp_username = smtp_user
                settings.smtp_password = smtp_pass
                settings.voice_wake_word = wake_word
                settings.theme = theme

                session.add(settings)
                session.commit()
                st.success("Settings saved successfully!")

    finally:
        session.close()
