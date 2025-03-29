import json, os
import requests
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load environment variables
load_dotenv()

# Load the resume JSON
with open('output.json', 'r') as file:
    resume_data = json.load(file)

def cal_score_based_on_wt(resume_data):
    # Define weights and caps
    weights = {
        'copyright': 2.5,
        'certificate': 1.0,
        'publication': 4.0,
        'project and their description': 2.5
    }
    
    caps = {
        'copyright': 1,
        'certificate': 2,
        'publication': 1,
        'project and their description': 2
    }

    # Get actual counts
    counts = {
        'copyright': len(resume_data.get('copyright', [])),
        'certificate': len(resume_data.get('certificate', [])),
        'publication': len(resume_data.get('publication', [])),
        'project and their description': len(resume_data.get('project and their description', {}))
    }

    # Calculate scores
    raw_score = 0
    max_raw_score = 0

    for key in weights:
        capped_count = min(counts[key], caps[key])
        raw_score += capped_count * weights[key]
        max_raw_score += caps[key] * weights[key]

    final_score = round((raw_score / max_raw_score) * 10, 2)
    print(f"📊 Weighted Resume Score: {final_score} / 10")
    return final_score


    

# Job description input
job_description = """
Looking for a financial analyst with experience in financial reporting, budgeting, ERP tools like DEAMS or SAP, and strong analytical thinking.
"""

# Step 1: Extract and concatenate relevant fields
def build_resume_text(data: dict) -> str:
    skills = ', '.join(data.get("skills", []))
    certificates = ', '.join(data.get("certificate", []))
    projects = ' '.join([f"{proj}: {desc}" for proj, desc in data.get("project and their description", {}).items()])
    bio = f"Total Experience: {data.get('number of year timeline', '')}, Companies: {', '.join(data.get('company names', []))}"
    
    combined_text = f"{skills}\n{certificates}\n{projects}\n{bio}"
    # print(combined_text)
    return combined_text

# Step 2: Get Jina embedding
def get_jina_embedding(text: str):
    api_key = os.getenv("JINA_API_KEY")
    # print(api_key)
    URL = "https://api.jina.ai/v1/embeddings"

    response = requests.post(
        URL,
        headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
          },
        json={
            "input": text,
            "model": "jina-embeddings-v3",
            "task": "classification"
        }
    )

    # try:
    #     response_data = response.json()
    #     if 'data' in response_data and len(response_data['data']) > 0:
    #         return response_data['data'][0]['embedding']
    #     else:
    #         print("Unexpected API response structure:", response_data)
    #         return None
    # except json.JSONDecodeError as e:
    #     print("Failed to decode JSON response:", e)
    #     return None

    return response.json()["data"][0]["embedding"] if response.status_code == 200 else None



# Step 3: Compute similarity score
def calculate_matching_score(embedding1 : np.ndarray, embedding2 : np.ndarray):
    sim = cosine_similarity(embedding1, embedding2)
    return sim * 100  # Return score as percentage

# Build texts
# resume_text = build_resume_text(resume_data)

# # Get embeddings
# resume_embedding = np.array(get_jina_embedding(resume_text)).reshape(1,-1)
# jd_embedding = np.array(get_jina_embedding(job_description)).reshape(1,-1)

# # print(np.array(resume_embedding).shape)
# print(resume_embedding.shape)
# print(jd_embedding.shape)
# # Calculate score
# score = calculate_matching_score(resume_embedding, jd_embedding)
# print(f"\n🎯 Matching Score: {score}%")

cal_score_based_on_wt(resume_data)
