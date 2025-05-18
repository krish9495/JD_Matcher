# main.py
import os
from app.parser import extract_text
from app.preprocessor import clean_text
from app.vectorizer import vectorize_texts
from app.ranker import rank_resumes

resumes_dir = "resumes/"
jd_path = "Job_descriptions/HappyFox_JD.pdf"  # Updated to match actual file name

# Load and preprocess JD
jd_text = clean_text(extract_text(jd_path))

# Load and preprocess resumes
resume_texts = []
resume_files = []

for file in os.listdir(resumes_dir):
    if file.endswith((".pdf", ".docx")):
        path = os.path.join(resumes_dir, file)
        raw = extract_text(path)
        resume_texts.append(clean_text(raw))
        resume_files.append(file)

# Vectorize
documents = [jd_text] + resume_texts
tfidf_matrix = vectorize_texts(documents)

# Rank
rankings = rank_resumes(tfidf_matrix)

# Show Results
print("\nRanked Resumes:")
for idx, score in rankings:
    print(f"{resume_files[idx]} — Score: {score:.4f}")
 