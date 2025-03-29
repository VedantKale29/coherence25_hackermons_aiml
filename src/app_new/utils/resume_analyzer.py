import streamlit as st
import random
import time
import re
import uuid
from datetime import datetime
import numpy as np

def analyze_resume(file, job_details):
    """
    Analyze a resume against job requirements
    In a real implementation, this would use NLP and ML to analyze the resume
    """
    # Simulate processing time
    time.sleep(0.5 + random.random())
    
    # Mock analysis results
    skills_match = random.randint(60, 95)
    experience_match = random.randint(70, 95)
    education_match = random.randint(65, 95)
    
    # Calculate overall score
    overall_score = int((skills_match * 0.5) + (experience_match * 0.3) + (education_match * 0.2))
    
    # Mock extracted skills
    all_skills = ["Python", "JavaScript", "Java", "C++", "C#", "React", "Angular", "Vue", "Node.js", 
                 "Django", "Flask", "Spring", "SQL", "NoSQL", "AWS", "Azure", "GCP", "Docker", 
                 "Kubernetes", "CI/CD", "Git", "Agile", "Scrum", "TDD", "DevOps"]
    
    # Include some job skills and some random skills
    extracted_skills = []
    job_skills = job_details.get('skills', [])
    
    for skill in job_skills:
        if random.random() > 0.3:  # 70% chance to include each job skill
            extracted_skills.append(skill)
    
    # Add some random skills
    remaining_skills = [s for s in all_skills if s not in extracted_skills]
    extracted_skills.extend(random.sample(remaining_skills, min(5, len(remaining_skills))))
    
    # Mock extracted experience
    experience_years = random.randint(1, 10)
    
    # Mock extracted education
    education_options = ["Bachelor's in Computer Science", "Master's in IT", "PhD in Data Science", 
                        "Bachelor's in Engineering", "Master's in Computer Engineering"]
    education = random.choice(education_options)
    
    # Generate skill proficiency levels
    skill_proficiency = {}
    for skill in extracted_skills:
        skill_proficiency[skill] = random.randint(60, 100)
    
    # Generate work history
    work_history = []
    current_year = datetime.now().year
    current_month = datetime.now().month
    
    for i in range(random.randint(1, 3)):
        duration = random.randint(12, 36)  # Duration in months
        end_year = current_year - (i * 2)
        end_month = random.randint(1, 12)
        
        start_year = end_year - (duration // 12)
        start_month = end_month - (duration % 12)
        if start_month <= 0:
            start_month += 12
            start_year -= 1
        
        company_names = ["TechCorp", "InnovateSoft", "DataSystems", "CloudTech", "DevSolutions", "AILabs", "CodeWorks"]
        job_titles = ["Software Engineer", "Data Scientist", "Full Stack Developer", "DevOps Engineer", "Product Manager", "UX Designer"]
        
        work_history.append({
            "company": random.choice(company_names),
            "title": random.choice(job_titles),
            "start_date": f"{start_year}-{start_month:02d}",
            "end_date": f"{end_year}-{end_month:02d}" if i > 0 else "Present",
            "duration": f"{duration // 12} years, {duration % 12} months"
        })
    
    # Return analysis results
    return {
        "score": overall_score,
        "skills_match": skills_match,
        "experience_match": experience_match,
        "education_match": education_match,
        "extracted_skills": extracted_skills,
        "skill_proficiency": skill_proficiency,
        "experience_years": experience_years,
        "education": education,
        "work_history": work_history
    }

def verify_resume(file):
    """
    Verify a resume for authenticity and potential issues
    In a real implementation, this would use AI to detect suspicious patterns
    """
    # Simulate processing time
    time.sleep(0.2 + random.random() * 0.5)
    
    # Randomly mark some resumes as suspicious (15% chance)
    is_suspicious = random.random() < 0.15
    
    if is_suspicious:
        # Generate a random reason for suspicion
        reasons = [
            "Inconsistent employment dates detected",
            "Suspicious qualification claims",
            "Potential keyword stuffing detected",
            "Unusual formatting patterns",
            "Mismatched skills and experience",
            "Potentially fabricated references",
        ]
        
        reason = random.choice(reasons)
        confidence = 70 + random.randint(0, 25)  # 70-95% confidence
        
        return {
            "suspicious": True,
            "message": f"{reason} ({confidence}% confidence)",
            "confidence": confidence
        }
    else:
        return {
            "suspicious": False,
            "message": "Resume verified successfully",
            "confidence": 95 + random.randint(0, 5)  # 95-100% confidence
        }

def extract_contact_info(file):
    """
    Extract contact information from a resume
    In a real implementation, this would use NLP to extract contact details
    """
    # Mock extracted contact info
    first_names = ["John", "Emily", "Michael", "Sarah", "David", "Jennifer", "Robert", "Lisa", "William", "Jessica"]
    last_names = ["Smith", "Johnson", "Chen", "Williams", "Rodriguez", "Brown",  "Jessica"]
    last_names = ["Smith", "Johnson", "Chen", "Williams", "Rodriguez", "Brown", "Davis", "Miller", "Wilson", "Moore"]
    
    name = random.choice(first_names) + " " + random.choice(last_names)
    email = name.lower().replace(" ", ".") + "@example.com"
    phone = f"+1 (555) {random.randint(100, 999)}-{random.randint(1000, 9999)}"
    
    # Generate additional contact details
    locations = ["San Francisco, CA", "New York, NY", "Seattle, WA", "Austin, TX", "Boston, MA"]
    linkedin = f"linkedin.com/in/{name.lower().replace(' ', '-')}"
    github = f"github.com/{name.lower().split()[0]}"
    
    return {
        "name": name,
        "email": email,
        "phone": phone,
        "location": random.choice(locations),
        "linkedin": linkedin,
        "github": github
    }

def generate_personality_assessment():
    """
    Generate a mock personality assessment
    In a real implementation, this would use AI to analyze personality traits
    """
    traits = {
        "analytical": random.randint(60, 100),
        "creative": random.randint(60, 100),
        "detail_oriented": random.randint(60, 100),
        "leadership": random.randint(60, 100),
        "teamwork": random.randint(60, 100),
        "communication": random.randint(60, 100),
        "problem_solving": random.randint(60, 100),
        "adaptability": random.randint(60, 100)
    }
    
    # Generate a personality description based on top traits
    top_traits = sorted(traits.items(), key=lambda x: x[1], reverse=True)[:3]
    
    descriptions = {
        "analytical": "Shows strong analytical thinking and data-driven decision making.",
        "creative": "Demonstrates creative problem-solving and innovative thinking.",
        "detail_oriented": "Exhibits excellent attention to detail and thoroughness.",
        "leadership": "Displays natural leadership qualities and initiative.",
        "teamwork": "Excels in collaborative environments and team settings.",
        "communication": "Possesses strong communication skills, both written and verbal.",
        "problem_solving": "Demonstrates exceptional problem-solving abilities.",
        "adaptability": "Shows great adaptability and flexibility in changing situations."
    }
    
    assessment = " ".join([descriptions[trait] for trait, _ in top_traits])
    
    return {
        "traits": traits,
        "assessment": assessment
    }

