import requests
import json
import os
import re
from dotenv import load_dotenv
from difflib import SequenceMatcher

load_dotenv()

def fetch_linkedin_data(linkedin_url: str) -> dict:
    api_key = os.getenv("PROXYCURL_API_KEY")
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    response = requests.get(
        "https://nubela.co/proxycurl/api/v2/linkedin",
        headers=headers,
        params={"url": linkedin_url}
    )
    
    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        return {}

    return response.json()

def similar(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def is_similar_in_list(target, list_values, threshold=0.75):
    return any(similar(target, val) >= threshold for val in list_values)

def validate_resume_with_linkedin(resume_path: str, linkedin_path: str) -> dict:
    with open(resume_path, 'r') as f:
        resume = json.load(f)

    with open(linkedin_path, 'r') as f:
        linkedin = json.load(f)

    # Flatten LinkedIn fields
    linkedin_companies = [exp.get("company", "").lower() for exp in linkedin.get("experiences", [])]
    linkedin_titles = [exp.get("title", "").lower() for exp in linkedin.get("experiences", [])]
    linkedin_schools = [edu.get("school", "").lower() for edu in linkedin.get("education", [])]
    linkedin_certs = [cert.get("name", "").lower() for cert in linkedin.get("certifications", [])]

    results = {
        "company_match": [],
        "education_match": [],
        "role_match": [],
        "certificate_match": [],
        "missing_in_linkedin": [],
        "resume_flagged_as_fake": False
    }

    # Flag if anything is missing
    def check_and_add(field_name, resume_list, linkedin_list):
        for item in resume_list:
            if is_similar_in_list(item, linkedin_list):
                results[f"{field_name}_match"].append(item)
            else:
                results["missing_in_linkedin"].append(f"{field_name.capitalize()}: {item}")
                results["resume_flagged_as_fake"] = True

    check_and_add("company", resume.get("company names", []), linkedin_companies)
    check_and_add("education", resume.get("education institute name", []), linkedin_schools)
    check_and_add("role", resume.get("role position in company", []), linkedin_titles)
    check_and_add("certificate", resume.get("certificate", []), linkedin_certs)

    return results

# --- Fetch LinkedIn data and save locally ---
linkedin_url = "https://www.linkedin.com/in/vedant-kale-b1836a25a/"
linkedin_data = fetch_linkedin_data(linkedin_url)

with open("linkdindata.json", 'w+') as file:
    json.dump(linkedin_data, file, indent=4)

# --- Match resume to LinkedIn ---
results = validate_resume_with_linkedin("output.json", "linkdindata.json")
print(json.dumps(results, indent=2))
