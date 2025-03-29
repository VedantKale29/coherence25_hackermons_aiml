import json
import re

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
