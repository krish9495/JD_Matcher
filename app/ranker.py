# app/ranker.py
from sklearn.metrics.pairwise import cosine_similarity

def rank_resumes(tfidf_matrix):
    jd_vector = tfidf_matrix[0]
    resume_vectors = tfidf_matrix[1:]
    scores = cosine_similarity(jd_vector, resume_vectors).flatten()
    return sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
