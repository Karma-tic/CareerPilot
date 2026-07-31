"""
Unit tests for CareerPilot AI File Export functions (CSV, Excel, JSON, PDF).
"""

from pathlib import Path
from utils import (
    export_jobs_to_csv,
    export_jobs_to_excel,
    export_jobs_to_json,
    export_jobs_to_pdf,
)


def test_export_functions(tmp_path):
    sample_jobs = [
        {
            "company": "Export Tech",
            "title": "Full Stack Dev",
            "salary": "$130,000",
            "location": "Remote",
            "source": "Test",
            "date_posted": "2026-07-31",
            "url": "https://example.com/job1",
            "skills": "Python, React",
        }
    ]

    csv_file = str(tmp_path / "test_jobs.csv")
    excel_file = str(tmp_path / "test_jobs.xlsx")
    json_file = str(tmp_path / "test_jobs.json")
    pdf_file = str(tmp_path / "test_jobs.pdf")

    p1 = export_jobs_to_csv(sample_jobs, output_path=csv_file)
    p2 = export_jobs_to_excel(sample_jobs, output_path=excel_file)
    p3 = export_jobs_to_json(sample_jobs, output_path=json_file)
    p4 = export_jobs_to_pdf(sample_jobs, output_path=pdf_file)

    assert Path(p1).exists()
    assert Path(p2).exists()
    assert Path(p3).exists()
    assert Path(p4).exists()
