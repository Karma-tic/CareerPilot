"""
CareerPilot AI - Main Application Entry Point
Launches Streamlit interface, initializes database schema, seeds sample data, and manages tab navigation.
"""

import streamlit as st
from config import logger, SettingsConfig
from database import db_manager
from scheduler import automation_scheduler
from dashboard import (
    apply_custom_css,
    render_overview_tab,
    render_job_listings_tab,
    render_applications_tab,
    render_analytics_tab,
    render_resume_match_tab,
    render_voice_automation_tab,
    render_settings_tab,
)

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="CareerPilot - Job Search & Intelligence Platform",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize Database Schema & Seed Data if needed
@st.cache_resource
def init_application_backend():
    logger.info("Initializing CareerPilot backend services...")
    db_manager.init_db()
    # Start automation scheduler
    automation_scheduler.start()
    return True

init_application_backend()

# Apply CSS Design System
apply_custom_css()

# Sidebar Navigation Header
st.sidebar.markdown(
    """
    <div style="text-align: center; padding: 12px 0;">
        <h1 style="color: #F5F3FF; margin:0; font-size: 1.8rem; font-weight:700;">CareerPilot</h1>
        <p style="color: #C4B5FD; font-size: 0.85rem;">Job Search & Executive Intelligence</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.divider()

# Navigation Tabs
menu_selection = st.sidebar.radio(
    "Navigation Menu",
    [
        "Overview",
        "Job Listings",
        "Application Tracker",
        "Analytics & Predictions",
        "AI Resume Matcher",
        "Voice & Automation",
        "Settings",
    ],
    index=0,
)

st.sidebar.divider()
st.sidebar.caption("CareerPilot v1.0.0 | Authentic Edition")

# Tab Router
if menu_selection == "Overview":
    render_overview_tab()
elif menu_selection == "Job Listings":
    render_job_listings_tab()
elif menu_selection == "Application Tracker":
    render_applications_tab()
elif menu_selection == "Analytics & Predictions":
    render_analytics_tab()
elif menu_selection == "AI Resume Matcher":
    render_resume_match_tab()
elif menu_selection == "Voice & Automation":
    render_voice_automation_tab()
elif menu_selection == "Settings":
    render_settings_tab()
