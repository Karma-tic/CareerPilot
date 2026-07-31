"""
CareerPilot AI - Modern Streamlit Dashboard UI Component
Contains custom natural & classy CSS theme, multi-layer location filters, interactive charts, and forms.
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


def apply_custom_css():
    """Inject a classy, authentic, natural CSS color theme into Streamlit."""
    st.markdown(
        """
        <style>
        /* Natural & Classy Color Palette */
        /* Background: Dark Warm Slate (#18181B / #27272A) */
        .stApp {
            background-color: #18181B;
            color: #F5F5F4;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #111827;
            border-right: 1px solid #374151;
        }
        
        /* Metric Card Styling - Natural Emerald & Gold accents */
        div[data-testid="stMetricValue"] {
            font-size: 2.1rem !important;
            font-weight: 700 !important;
            color: #10B981 !important; /* Natural Emerald */
        }
        
        div[data-testid="stMetric"] {
            background: #27272A;
            border: 1px solid #3F3F46;
            border-radius: 10px;
            padding: 16px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        }

        /* Buttons Styling - Forest Emerald & Natural Slate */
        .stButton > button {
            background: linear-gradient(135deg, #059669 0%, #047857 100%);
            color: #FFFFFF;
            border: 1px solid #065F46;
            border-radius: 8px;
            font-weight: 600;
            padding: 0.5rem 1.2rem;
            transition: all 0.2s ease-in-out;
        }
        .stButton > button:hover {
            background: linear-gradient(135deg, #10B981 0%, #059669 100%);
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
            border-color: #34D399;
        }
        
        /* Classy Badges */
        .badge-applied { background-color: #1E293B; color: #94A3B8; padding: 4px 10px; border-radius: 6px; font-size: 0.85rem; font-weight: 600; border: 1px solid #475569; }
        .badge-interview { background-color: #78350F; color: #FDE68A; padding: 4px 10px; border-radius: 6px; font-size: 0.85rem; font-weight: 600; border: 1px solid #92400E; }
        .badge-offer { background-color: #064E3B; color: #A7F3D0; padding: 4px 10px; border-radius: 6px; font-size: 0.85rem; font-weight: 600; border: 1px solid #047857; }
        .badge-rejected { background-color: #7F1D1D; color: #FCA5A5; padding: 4px 10px; border-radius: 6px; font-size: 0.85rem; font-weight: 600; border: 1px solid #991B1B; }
        
        /* Job Card Styling */
        .job-card {
            background-color: #27272A;
            border: 1px solid #3F3F46;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
        }

        .location-tag {
            background-color: #3F3F46;
            color: #E7E5E4;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: 500;
        }
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
    """Render 🔍 Job Listings Page with search and multi-layer location filters (City -> State -> Scope)."""
    st.header("🔍 Job Search & Location Filters")
    st.caption("Hierarchical location filtering (Bhopal -> MP -> National/Remote) and 1-click tracking.")

    # Multi-Layer Location Filter Bar
    with st.expander("🌐 Hierarchical Location & Search Filters", expanded=True):
        f_col1, f_col2, f_col3, f_col4, f_col5 = st.columns(5)
        with f_col1:
            search_query = st.text_input("Keywords", placeholder="e.g. Python, AI, Developer")
        with f_col2:
            city_filter = st.selectbox("Layer 1: City / Local", ["All Cities", "Bhopal", "Indore", "Bangalore", "Mumbai", "Pune", "Delhi NCR", "Remote"])
        with f_col3:
            state_filter = st.selectbox("Layer 2: State / Region", ["All States", "Madhya Pradesh", "Karnataka", "Maharashtra", "Delhi", "Remote"])
        with f_col4:
            scope_filter = st.selectbox("Layer 3: Scope", ["All Work Types", "Remote Only", "Hybrid", "On-site"])
        with f_col5:
            run_scraper = st.button("Scrape Jobs")

    if run_scraper:
        with st.spinner("Scraping job portals with location filters..."):
            kws = [search_query] if search_query else None
            is_rem = scope_filter == "Remote Only"
            is_hyb = scope_filter == "Hybrid"
            saved = job_scraper.run_scraping_cycle(
                is_remote=is_rem,
                is_hybrid=is_hyb,
                city=None if city_filter == "All Cities" else city_filter,
                state=None if state_filter == "All States" else state_filter,
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
        if city_filter != "All Cities":
            query = query.filter(Job.city.ilike(f"%{city_filter}%"))
        if state_filter != "All States":
            query = query.filter(Job.state.ilike(f"%{state_filter}%"))
        if scope_filter == "Remote Only":
            query = query.filter(Job.location.ilike("%Remote%"))
        elif scope_filter == "Hybrid":
            query = query.filter(Job.location.ilike("%Hybrid%"))

        jobs = query.order_by(Job.id.desc()).all()
        st.write(f"Showing **{len(jobs)}** matching job opportunities:")

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
        for j in jobs[:25]:
            with st.container():
                st.markdown(
                    f"""
                    <div class="job-card">
                        <h3 style="color:#10B981; margin-bottom:5px;">{j.title}</h3>
                        <p style="color:#D4D4D8; font-size:1.0rem;"><strong>{j.company}</strong> • <span class="location-tag">📍 {j.city or 'Bhopal'}, {j.state or 'MP'}</span> • <span style="color:#F59E0B; font-weight:600;">{j.salary}</span></p>
                        <p style="color:#A1A1AA; font-size:0.9rem;">{j.description[:250]}...</p>
                        <p style="color:#71717A; font-size:0.85rem;"><strong>Skills:</strong> {j.skills or 'Python, Engineering'}</p>
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
            theme = st.selectbox("UI Theme", ["natural", "dark"], index=0)

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
