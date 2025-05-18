# app/vectorizer.py
from sklearn.feature_extraction.text import TfidfVectorizer

def vectorize_texts(text_list):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(text_list)
    return tfidf_matrix
