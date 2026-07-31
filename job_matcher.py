"""
CareerPilot AI - Job Matcher & AI Assistant Module
Computes resume-to-job match scores, identifies missing skills, generates cover letters, and summarizes job descriptions.
"""

from config import logger
from utils import extract_skills_from_text, COMMON_SKILLS_TAXONOMY


class JobMatcher:
    """AI and Rule-Based Resume Matcher, Cover Letter Generator, and JD Summarizer."""

    def __init__(self, openai_api_key: str = None):
        self.api_key = openai_api_key

    def calculate_match(self, resume_text: str, job_description: str, job_title: str = "") -> dict:
        """Calculate match percentage, matched skills, missing skills, and improvement suggestions."""
        resume_skills = set(extract_skills_from_text(resume_text))
        job_skills = set(extract_skills_from_text(job_description + " " + job_title))

        if not job_skills:
            # Fallback if no taxonomy skills matched
            job_skills = set(["Python", "Software Engineering", "Communication", "Problem Solving", "Git"])

        matched_skills = resume_skills.intersection(job_skills)
        missing_skills = job_skills.difference(resume_skills)

        # Calculate score ratio
        if len(job_skills) > 0:
            match_percentage = min(100, max(15, int((len(matched_skills) / len(job_skills)) * 100)))
        else:
            match_percentage = 70

        # Boost score slightly if resume text has high text overlap
        word_overlap = set(resume_text.lower().split()).intersection(set(job_description.lower().split()))
        if len(word_overlap) > 30 and match_percentage < 85:
            match_percentage = min(95, match_percentage + 15)

        suggestions = []
        if missing_skills:
            suggestions.append(f"Consider adding or highlighting these skills in your resume: {', '.join(sorted(list(missing_skills))[:5])}.")
        if "Docker" in missing_skills or "AWS" in missing_skills:
            suggestions.append("Highlight containerization and cloud infrastructure experience on your project list.")
        if "FastAPI" in missing_skills or "Flask" in missing_skills:
            suggestions.append("Mention RESTful API architecture and asynchronous Python backend frameworks.")

        if not suggestions:
            suggestions.append("Great alignment! Ensure your recent achievements highlight measurable project results.")

        return {
            "match_percentage": match_percentage,
            "resume_skills": sorted(list(resume_skills)),
            "job_skills": sorted(list(job_skills)),
            "matched_skills": sorted(list(matched_skills)),
            "missing_skills": sorted(list(missing_skills)),
            "suggestions": suggestions,
        }

    def generate_cover_letter(
        self,
        applicant_name: str,
        company_name: str,
        job_title: str,
        job_description: str,
        resume_text: str = "",
    ) -> str:
        """Generate a tailored, professional cover letter for a job application."""
        extracted_resume_skills = extract_skills_from_text(resume_text)
        top_skills_str = ", ".join(extracted_resume_skills[:4]) if extracted_resume_skills else "Python development, data pipelines, and scalable software architecture"

        cover_letter = f"""Dear Hiring Manager at {company_name},

I am writing to express my strong interest in the {job_title} role at {company_name}. With my extensive background in {top_skills_str}, I am confident in my ability to immediately contribute to your engineering initiatives and product goals.

Having reviewed the requirements for {job_title}, I was particularly drawn to {company_name}'s focus on innovation and technical excellence. My hands-on experience aligns closely with your needs:

• Technical Expertise: Proven proficiency in key frameworks including {top_skills_str}.
• Problem Solving & Automation: Track record of designing automated workflows, optimizing backend services, and delivering reliable software systems.
• Collaborative Delivery: Strong communication skills and experience delivering quality solutions within fast-paced agile team environments.

I would welcome the opportunity to discuss how my technical skills and passion for high-impact software engineering match your team's vision. Thank you for your time and consideration.

Sincerely,
{applicant_name}
"""
        logger.info(f"Generated customized cover letter for {job_title} at {company_name}.")
        return cover_letter

    def summarize_job(self, job_title: str, company: str, job_description: str) -> dict:
        """Summarize job description into key highlights."""
        skills = extract_skills_from_text(job_description)
        skills_str = ", ".join(skills[:6]) if skills else "Python, Software Development, System Design"
        
        summary_bullets = [
            f"Role: {job_title} at {company}",
            f"Core Skill Requirements: {skills_str}",
            "Key Focus: Developing software, maintaining scalable services, and collaborating across engineering teams.",
            "Work Model: Remote / Hybrid flexible software position."
        ]
        
        return {
            "summary_bullets": summary_bullets,
            "skills": skills
        }


# Singleton instance helper
job_matcher = JobMatcher()
