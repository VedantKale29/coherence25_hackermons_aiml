'''
This module is responsible for dealing with text. Includes three sub-modules :
1. text extraction from pdf - done
2. text cleaning functions - done
3. skills extraction from text - done
'''
from typing import List, Tuple, Union
from enum import Enum
from pydantic import SecretStr
from pypdf import PdfReader
from langchain_community.document_loaders import PyPDFLoader
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_groq.chat_models import ChatGroq
from langchain.document_loaders import PyMuPDFLoader
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

# # Extract text from a PDF file
# reader = PyMuPDFLoader("10554236.pdf")
# documents = reader.load()  # Returns a list of Document objects

# # Extract text from each page
# text = ""
# for doc in documents:
#     text += doc.page_content + "\n"

# # Print extracted text
# print(text)


stop_words = set(stopwords.words('english'))

class TextLoader(Enum):
    Langchain_loader = PyMuPDFLoader
    Pypdf = PdfReader
    pass



def extract_text_from_pdf(pdf_path: str, loader : TextLoader = TextLoader.Langchain_loader) -> str:
    reader = PyMuPDFLoader(pdf_path)
    documents = reader.load()  # Returns a list of Document objects
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

def preprocess_text(
        text: str, 
        extra_info = False, 
        objects  = PorterStemmer()
        ) -> Union[str, Tuple[str, List[str], List[str]]]:

    ps = objects
    #lowercasing
    text = text.lower()
    # remove special characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    #remove hastags and mentions
    user_mentions = re.findall(r'@\w+', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'#\w+', '', text)
    #Store urls -> may contain github/linkedin links
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    text = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    # remove stop words
    text = ' '.join([word for word in text.split() if word not in stop_words])
    #lemmatization
    text = ' '.join([ps.stem(word) for word in word_tokenize(text)])
    if extra_info:
        return text, urls, user_mentions
    return text



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
    "skills or languages or framework": [...],
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
    "role and their description": {
        "role name": "short description"
    },
    "project and their description": {
        "project name": "short description"
    },
    "extra curricular activity": [...],
    "phone number": "...",
    "mail id": "..."
    "github.com": "...",
    "linkedin.com": "...",
    
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


pdf_path = "vedant.pdf"
resume_text = extract_text_from_pdf(pdf_path)
extracted_data = skills_extraction(resume_text)