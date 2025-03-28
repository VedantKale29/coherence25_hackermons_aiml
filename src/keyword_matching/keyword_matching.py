def keyword_matching_overlap(jd_keywords, resume_keywords):
    jd_keywords = jd_keywords.split(',')
    resume_keywords = resume_keywords.split(',')
    jd_keywords = [e.strip() for e in jd_keywords]
    resume_keywords = [e.strip() for e in resume_keywords]
    
    percentage_skill = len(set(jd_keywords).intersection(set(resume_keywords))) / len(set(jd_keywords))
    return percentage_skill