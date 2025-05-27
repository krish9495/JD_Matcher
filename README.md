# 📄 AI Resume Ranking Tool

A smart Python-based command-line tool that ranks resumes against a job description using TF-IDF vectorization, cosine similarity, and section-aware text parsing.

---

## 🚀 Features

- Upload one **Job Description** (PDF)
- Upload multiple **Resumes** (PDF/DOCX/TXT)
- Parses each resume section-wise: **skills, experience, education, projects**
- Uses **TF-IDF vectorization** and **cosine similarity** for scoring
- Outputs a **ranked list** with **score breakdowns**
- Runs via CLI and prints results in a readable format

---

## 🧠 Tech Stack

| Purpose        | Tools/Libs Used         |
|----------------|-------------------------|
| Parsing        | PyMuPDF, python-docx    |
| NLP            | NLTK                    |
| Vectorization  | Scikit-learn TF-IDF     |
| Similarity     | Cosine Similarity       |
| CLI Interface  | Python (main.py script) |

---

## 🗂️ Project Structure
```
resume-ranker/
├── app/
│ ├── resume_ranker.py # Core ranking logic
│ ├── text_extractor.py # Resume & JD parser
│ └── utils/ # Any helper functions
├── resumes/ # Folder for uploaded resumes
├── Job_descriptions/ # Folder for the job description
├── main.py # CLI entry point
├── requirements.txt
└── README.md
```

---

## ⚙️ How to Run

1. Install requirements:

```bash
pip install -r requirements.txt
````
Add:

Resumes to resumes/

A job description file named job_description.pdf to Job_descriptions/

### Run the script:
python main.py

### View the ranked output with breakdowns like:

1. John_Doe.pdf
   Skills Score: 82%
   Experience Score: 76%
   Education Score: 60%
   Projects Score: 70%
   Total Score: 72%
   
## 📈 Future Improvements
Add keyword-based skill matching

Visualize results in web interface (React or Streamlit)

Export results to CSV

Add configurable scoring weights per section

Optional upgrade to BERT embeddings in future phase
