'''
This module dealings with the scoring logic.
Includes two sub-modules:
1. skill overlap calc - done
2. similarity score using tf-idf (no vector embeddings since the corpus is small and the text is domain-specific) - done
'''
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def skill_overlap_calc(skill_set1, skill_set2):
    
    skill_overlap = len(set(skill_set1).intersection(set(skill_set2)))
    return skill_overlap

def similarity_score_calc(text1, text2, objects = TfidfVectorizer()):

    tf_idf_obj = objects
    tf_idf_1 = tf_idf_obj.fit_transform(text1)
    tf_idf_2 = tf_idf_obj.transform(text2)
    similarity_score = cosine_similarity(tf_idf_1, tf_idf_2)
    return similarity_score[0][0]

similarity_score_calc([1,1,1], [2,2,2])