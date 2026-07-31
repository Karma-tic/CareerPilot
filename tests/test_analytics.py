"""
Unit tests for CareerPilot AI Analytics Engine.
"""

import pandas as pd
import pytest
from database import db_manager
from analytics import analytics_engine


@pytest.fixture(autouse=True)
def setup_database():
    """Ensure database tables are initialized and seeded before running analytics tests."""
    db_manager.init_db()


def test_analytics_dataframes():
    df_jobs = analytics_engine.get_jobs_dataframe()
    df_apps = analytics_engine.get_applications_dataframe()

    assert isinstance(df_jobs, pd.DataFrame)
    assert isinstance(df_apps, pd.DataFrame)


def test_plotly_chart_generators():
    df_jobs = analytics_engine.get_jobs_dataframe()
    df_apps = analytics_engine.get_applications_dataframe()

    fig_time = analytics_engine.create_applications_over_time_chart(df_apps)
    fig_salary = analytics_engine.create_salary_distribution_chart(df_jobs)
    fig_skills = analytics_engine.create_skills_frequency_chart(df_jobs)
    fig_ratio = analytics_engine.create_interview_ratio_chart(df_apps)

    assert fig_time is not None
    assert fig_salary is not None
    assert fig_skills is not None
    assert fig_ratio is not None


def test_predictions():
    valuable_skills = analytics_engine.predict_valuable_skills()
    assert isinstance(valuable_skills, list)
    assert len(valuable_skills) > 0
