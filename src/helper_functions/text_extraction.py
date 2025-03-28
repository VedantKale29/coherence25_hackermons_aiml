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

# Extract text from a PDF file
reader = PyMuPDFLoader("10554236.pdf")
documents = reader.load()  # Returns a list of Document objects

# Extract text from each page
text = ""
for doc in documents:
    text += doc.page_content + "\n"

# Print extracted text
print(text)


stop_words = set(stopwords.words('english'))

class TextLoader(Enum):
    Langchain_loader = PyMuPDFLoader
    Pypdf = PdfReader
    pass

def extract_text_from_pdf(pdf_path, loader : TextLoader = TextLoader.Langchain_loader):
    # reader = PdfReader(pdf_path)
    # text = ''
    # for page in reader.pages:
    #     text += page.extract_text()
    # return text
    reader = PyMuPDFLoader(pdf_path)
    documents = reader.load()  # Returns a list of Document objects

    # Extract text from each page
    text = ""
    for doc in documents:
        text += doc.page_content + "\n"
    return text

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

def skills_extraction(text : str, secret_key:SecretStr, model_id:str) -> None:
    
    #defining objects
    parser = JsonOutputParser()
    llm = ChatGroq(
        api_key=secret_key,
        model = model_id
    )
    chat_prompt = ChatPromptTemplate.from_template(
        '''
        Assume you are a recruiter and you have to shortlist a candidate for a job.
        You have a resume of a candidate in text format.
        Return the output in json format only with one field only : "skills".
        The output should contain a list of skills extracted from the resume.
        Make sure to also include implicit skills that are not explicitly mentioned in the resume but are highlighted from the project and work experience.
        '''
    )

    #chain the functions

    output = chat_prompt | llm | parser
    print(output["skills"])
    return output["skills"]

# if __name__ == "__main__":
    skills_extraction