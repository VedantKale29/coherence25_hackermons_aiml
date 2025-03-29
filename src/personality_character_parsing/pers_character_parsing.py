from json import load
from pydantic import SecretStr
from langchain_groq import ChatGroq
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
import os
load_dotenv("./.env")

class PersonalityCharacterParser:
    def __init__(self, model_name: str):
        self.model_name = model_name
        # Load environment variables from .env file
        key = os.getenv("GROQ_API_KEY")
        self.llm = ChatGroq(
            api_key= SecretStr(key) if key is not None else None,
            model=model_name,
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )
        self.sentiment = SentimentIntensityAnalyzer()
        self.output_parser = JsonOutputParser()
        pass

    def parse_character(self, character_description: str, soft_skills: str, hobbies, job_description: str):
        prompt = ChatPromptTemplate.from_template(
            '''
            Suppose you are a personality character parser. You are given a character description, soft skills, hobbies of the applicant and the job description of the job. I want you to return two things in JSON format and nothing else:
            1. A short summary of the canditates personality traits. 
            2. A score from 0 to 100 for each of the personality traits, which gives a short summary of the personality of the applicant, where 0 means not at all and 100 means very much.
            
            The character description is: {character_description}
            The soft skills are: {soft_skills}
            The hobbies are: {hobbies}
            The job description is: {job_description}
            
            Return the response in this exact JSON format:
            {{
                "personality_traits": [The candiate is very hardworking, smart and concious with good leadership],
                "scores": 10
            }}
            '''
        )
    
        llm_chain = prompt | self.llm | self.output_parser
        result = llm_chain.invoke({
            "character_description": character_description,
            "soft_skills": soft_skills,
            "hobbies": hobbies,
            "job_description": job_description
        })
        return result
    
    def parse_sentiment(self, text: str, character_score : float):
        return character_score * self.sentiment.polarity_scores(text)['compound']
    

