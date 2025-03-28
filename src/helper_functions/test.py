import os
import json
from langchain_community.document_loaders import PyMuPDFLoader
from google import genai
from dotenv import load_dotenv
import re

def extract_json_from_string(text: str) -> str:
    """
    Extracts and fixes JSON block from a text response.
    """
    try:
        # Try parsing raw first
        return json.loads(text)
    except json.JSONDecodeError:
        # Fallback: Try to fix common issues
        cleaned_text = text.strip()
        cleaned_text = re.sub(r"```json|```", "", cleaned_text)
        cleaned_text = re.sub(r",\s*}", "}", cleaned_text)
        cleaned_text = re.sub(r",\s*]", "]", cleaned_text)
        try:
            return json.loads(cleaned_text)
        except Exception as e:
            print("Still failing after cleanup:", e)
            print("Content:\n", cleaned_text)
            raise e


# Load environment variables from the .env file
load_dotenv()

# Retrieve the Gemini API key from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Initialize the Gemini client with the API key
client = genai.Client(api_key=gemini_api_key)

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from a PDF file using PyMuPDFLoader.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The extracted text.
    """
    loader = PyMuPDFLoader(pdf_path)
    documents = loader.load()
    text = "\n".join(doc.page_content for doc in documents)
    return text

def count_tokens(text: str) -> int:
    """
    Counts the number of tokens in the given text.

    Args:
        text (str): The input text.

    Returns:
        int: The number of tokens.
    """
    # Tokenization logic depends on the tokenizer used by the Gemini model
    # Placeholder function: replace with actual token counting logic
    return len(text.split())

def skills_extraction(text: str, model: str = "gemini-1.5-flash") -> dict:
    """
    Extracts structured information from resume text using Gemini's API.

    Args:
        text (str): The resume text.
        model (str): The Gemini model to use.

    Returns:
        dict: Extracted information in JSON format.
    """
    system_prompt = """
    You are a technical recruiter AI. Extract the following information from a candidate's resume in **valid JSON format**.

    Return ONLY JSON. Do not include any explanations, notes, or comments.

    Required JSON Structure:
    {
    "skills": [...],
    "publication": [...],
    "certificate": [...],
    "company names": [...],
    "number of year timeline": "...",
    "education institute name": [...],
    "total time in company": "...",
    "passing year": [...],
    "marks in each degree with degree name": {
        "degree name": "grade or GPA"
    },
    "role position in company": [...],
    "project and their description": {
        "project name": "short description"
    },
    "extra curricular activity": [...],
    "phone number": "...",
    "mail id": "..."
    }

    Include implicit skills if they are clearly demonstrated in projects or experience.

    If a field is missing, return it with an empty list or null value.
    """


    # Check if the text exceeds the model's token limit
    max_tokens = 6000  # Example limit; adjust based on the specific model's capabilities
    if count_tokens(text) > max_tokens:
        raise ValueError("Input text exceeds the maximum token limit for the model.")

    response = client.models.generate_content(
        model=model,
        contents=[system_prompt + "\n\n" + text],
        config={
            "temperature": 0.2,
            "topP": 0.95,
            "topK": 40,
            "maxOutputTokens": 1024
        }
    )

    try:
        content = response.text
        output_file = 'output.json'
        data = json.loads(content)
        with open(output_file, 'w+') as file:
            json.dump(data, file, indent=4)
        current_directory = os.getcwd()
        print(f"The current working directory is: {current_directory}")
        return data
    except json.JSONDecodeError as e:
        print("❌ Failed to parse response:", e)
        print("Raw response:", content)
        output_file = 'output.json'
        # data = json.loads(content)
        data = extract_json_from_string(content)

        with open(output_file, 'w+') as file:
            json.dump(data, file, indent=4)
        return {}

# Example usage:
pdf_path = "10554236.pdf"
resume_text = extract_text_from_pdf(pdf_path)
extracted_data = skills_extraction(resume_text)
# print(extracted_data)
