"""
CareerPilot AI - Utility Functions Module
Provides multi-format file exporters (CSV, Excel, PDF, JSON), skill extraction helpers, and text processing tools.
"""

import json
import re
from pathlib import Path
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from config import EXPORTS_DIR, logger


# Known technical & professional skills dictionary for extraction
COMMON_SKILLS_TAXONOMY = [
    "Python", "Java", "C++", "C#", "JavaScript", "TypeScript", "HTML", "CSS", "SQL",
    "PostgreSQL", "MySQL", "SQLite", "MongoDB", "Redis", "Docker", "Kubernetes", "AWS",
    "Azure", "GCP", "FastAPI", "Flask", "Django", "Streamlit", "React", "Vue", "Angular",
    "Node.js", "PyTorch", "TensorFlow", "Scikit-Learn", "Pandas", "NumPy", "Plotly",
    "OpenAI API", "LangChain", "LLM", "RAG", "Playwright", "Selenium", "BeautifulSoup",
    "Git", "CI/CD", "Linux", "REST", "GraphQL", "Agile", "Scrum", "Data Science", "System Design"
]


def extract_skills_from_text(text: str) -> list[str]:
    """Extract known technical skills from text using regex matching."""
    if not text:
        return []
    
    extracted = set()
    for skill in COMMON_SKILLS_TAXONOMY:
        # Match whole word pattern case-insensitively
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text, re.IGNORECASE):
            extracted.add(skill)
            
    return sorted(list(extracted))


def export_jobs_to_csv(jobs_data: list[dict], output_path: str = None) -> str:
    """Export job listings to CSV format."""
    if output_path is None:
        output_path = str(EXPORTS_DIR / "jobs_export.csv")
    
    df = pd.DataFrame(jobs_data)
    df.to_csv(output_path, index=False, encoding="utf-8")
    logger.info(f"Jobs successfully exported to CSV: {output_path}")
    return output_path


def export_jobs_to_excel(jobs_data: list[dict], output_path: str = None) -> str:
    """Export job listings to Excel format (.xlsx)."""
    if output_path is None:
        output_path = str(EXPORTS_DIR / "jobs_export.xlsx")
        
    df = pd.DataFrame(jobs_data)
    df.to_excel(output_path, index=False, engine="openpyxl")
    logger.info(f"Jobs successfully exported to Excel: {output_path}")
    return output_path


def export_jobs_to_json(jobs_data: list[dict], output_path: str = None) -> str:
    """Export job listings to JSON format."""
    if output_path is None:
        output_path = str(EXPORTS_DIR / "jobs_export.json")
        
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(jobs_data, f, indent=4)
        
    logger.info(f"Jobs successfully exported to JSON: {output_path}")
    return output_path


def export_jobs_to_pdf(jobs_data: list[dict], output_path: str = None, title: str = "CareerPilot AI - Job Listings Report") -> str:
    """Export job listings or report to PDF format using ReportLab."""
    if output_path is None:
        output_path = str(EXPORTS_DIR / "jobs_report.pdf")
        
    doc = SimpleDocTemplate(output_path, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=15
    )
    
    header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Helvetica-Bold',
        textColor=colors.white
    )
    
    cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#334155')
    )

    elements = []
    elements.append(Paragraph(title, title_style))
    elements.append(Paragraph(f"Generated automatically by CareerPilot AI | Total Jobs: {len(jobs_data)}", styles['Normal']))
    elements.append(Spacer(1, 15))

    # Prepare table headers and rows
    table_data = [[
        Paragraph("Company", header_style),
        Paragraph("Title", header_style),
        Paragraph("Salary", header_style),
        Paragraph("Location", header_style),
        Paragraph("Source", header_style),
    ]]

    for job in jobs_data[:50]:  # Limit to 50 rows for clean PDF layout
        table_data.append([
            Paragraph(str(job.get("company", "N/A")), cell_style),
            Paragraph(str(job.get("title", "N/A")), cell_style),
            Paragraph(str(job.get("salary", "N/A")), cell_style),
            Paragraph(str(job.get("location", "N/A")), cell_style),
            Paragraph(str(job.get("source", "N/A")), cell_style),
        ])

    table = Table(table_data, colWidths=[110, 160, 110, 110, 60])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')])
    ]))
    
    elements.append(table)
    doc.build(elements)
    logger.info(f"PDF successfully generated: {output_path}")
    return output_path
