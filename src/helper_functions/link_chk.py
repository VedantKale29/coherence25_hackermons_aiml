import requests
import json
import os
import re
from dotenv import load_dotenv
from difflib import SequenceMatcher

is_linkedin_url_present = 1

def detect_fake_resume_from_file(json_path: str) -> dict:
    # Load resume data from file
    with open("output.json", 'r') as file:
        resume_data = json.load(file)

    # Join all resume text for analysis
    resume_text = " ".join([
        ' '.join(resume_data.get("skills", [])),
        ' '.join(resume_data.get("certificate", [])),
        ' '.join(resume_data.get("company names", [])),
        ' '.join(resume_data.get("education institute name", [])),
        ' '.join(resume_data.get("extra curricular activity", [])),
        ' '.join(resume_data.get("mail id") or []),
        ' '.join(resume_data.get("phone number") or []),
        ' '.join(resume_data.get("linkedin") or []),
        ' '.join(resume_data.get("github") or []),
        ' '.join([
            f"{proj}: {desc}" for proj, desc in resume_data.get("project and their description", {}).items()
        ])
    ])

    suspicion_score = 0
    reasons = []

    # 1. GitHub or LinkedIn missing
    if not resume_data.get("github") and not resume_data.get("linkedin"):
        suspicion_score += 2.0
        reasons.append("Missing GitHub and LinkedIn")
    else:
        is_linkedin_url_present=1

    # 2. Contact info missing
    if not resume_data.get("mail id") and not resume_data.get("phone number"):
        suspicion_score += 1.5
        reasons.append("Missing phone number and email")

    # 3. No quantifiable metrics (%, $, time, etc.)
    if not re.search(r'\b\d+(\.\d+)?\s?(%|\$|usd|users|ms|seconds|months|years|billion|million|k)\b', resume_text.lower()):
        suspicion_score += 1.5
        reasons.append("No quantifiable achievements")

    # 4. Skills-experience mismatch
    if len(resume_data.get("skills", [])) > 15 and len(resume_data.get("project and their description", {})) < 1:
        suspicion_score += 2.0
        reasons.append("Many skills but no projects listed")

    # 5. Missing key sections
    if not resume_data.get("certificate") or not resume_data.get("project and their description"):
        suspicion_score += 2.0
        reasons.append("Missing certificates or projects")

    # 6. Language pattern heuristic (basic)
    avg_sentence_length = sum(len(s.split()) for s in resume_text.split('.') if s) / max(1, len(resume_text.split('.')))
    if avg_sentence_length > 25:
        suspicion_score += 1.0
        reasons.append("Overly generic sentence structure")

    # Output
    result = {
        "suspicion_score": round(min(suspicion_score, 10.0), 2),
        "suspicious": suspicion_score >= 5.0,
        "reasons": reasons
    }

    print(f"\n🚨 Fake Resume Detection Score: {result['suspicion_score']} / 10")
    if result["suspicious"]:
        print("⚠️ This resume is flagged as potentially fake.")
    else:
        print("✅ This resume appears genuine.")
    
    return result

# Run the module on your uploaded file
if __name__ == "__main__":
    detect_fake_resume_from_file("/mnt/data/output.json")

load_dotenv()
if is_linkedin_url_present == 1:
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
