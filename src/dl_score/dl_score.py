import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from dotenv import load_dotenv
import pickle
import torch

class DL_score:

    def __init__(self) -> None:
        pass
    
    def preprocess_data(self, json_data):

        #Preprocess skills
        skills = json_data["skills"].split(',')  
        skills = [e.strip() for e in skills][:2]

        #Preprocess degree to get top 4 degrees
        degrees = json_data["degree"].split(',')
        degrees = [e.strip() for e in degrees][:2]

        json_data["experience_requirements"] = self.parse_experience_req(json_data["experience_requirements"])

        json_data["job_responsibilities"] = self.preprocess_meaningful_missing_cols(json_data, "job_responsibilities")
        json_data["educational_institution_name_2"] = self.preprocess_meaningful_missing_cols(json_data, "educational_institution_name_2")
        json_data["role_positions_2"] = self.preprocess_meaningful_missing_cols(json_data, "role_positions_2")
        json_data["degree_names_2"] = self.preprocess_meaningful_missing_cols(json_data, "degree_names_2")
        json_data["degree_names_3"] = self.preprocess_meaningful_missing_cols(json_data, "degree_names_3")
        json_data["degree_names_4"] = self.preprocess_meaningful_missing_cols(json_data, "degree_names_4")

        job_position = self.tf_idf_vectorizer(json_data, "job_position")
        educational_requirements = self.tf_idf_vectorizer(json_data, "educational_requirements")
        experience_requirements = self.tf_idf_vectorizer(json_data, "experience_requirements")
        skills = self.tf_idf_vectorizer(pd.DataFrame(skills, columns = ["skills"]), "skills")
        degrees = self.tf_idf_vectorizer(pd.DataFrame(degrees, columns = ["degree"]), "degree")
        educational_institute = self.tf_idf_vectorizer(json_data, "educational_institute")
        role = self.tf_idf_vectorizer(json_data, "role")

        return pd.concat([job_position, educational_requirements, experience_requirements, skills, degrees, educational_institute, role], axis = 1)
    
    def inference_pipeline(self, json_data):
        # Load the model
        model = pickle.load(open("model.pkl", "rb"))
        model.eval()
        
        
        # Preprocess the data
        preprocessed_data = self.preprocess_data(json_data)
        
        # Make predictions
        with torch.no_grad():
            return model(preprocessed_data).detach().numpy()
    def tf_idf_vectorizer(self,json_data, column):    
        # Initialize vectorizer
        self.vectorizer = pickle.load(open(f"{column}_vectorizer.pkl", "rb"))
        
        # Fit and transform the column
        return self.vectorizer.transform(json_data[column]) 

    def parse_experience_req(self,exp_feature):

        #Read the first number encountered in the string
        return exp_feature.str.extract(r'(\d+)').astype(float)

    def preprocess_meaningful_missing_cols(self, json_data, feature, na_value = "MISSING"):
        
        return json_data[feature].fillna(na_value)