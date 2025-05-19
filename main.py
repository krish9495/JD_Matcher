# main.py
import os
import sys
from app.resume_ranker import ResumeRanker
from app.text_extractor import extract_text

def ensure_directories():
    """Ensure required directories exist."""
    directories = ['resumes', 'Job_descriptions']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

def get_resume_files():
    """Get list of resume files from the resumes directory."""
    resume_files = []
    for file in os.listdir('resumes'):
        if file.endswith(('.pdf', '.docx', '.txt')):
            resume_files.append(os.path.join('resumes', file))
    return resume_files

def main():
    try:
        # Ensure directories exist
        ensure_directories()
        
        # Check for job description
        jd_path = os.path.join('Job_descriptions', 'job_description.pdf')
        if not os.path.exists(jd_path):
            print(f"Error: Job description not found at {jd_path}")
            print("Please place your job description PDF in the Job_descriptions directory.")
            return
        
        # Get resume files
        resume_files = get_resume_files()
        if not resume_files:
            print("Error: No resume files found in the resumes directory.")
            print("Please place resume files (PDF, DOCX, or TXT) in the resumes directory.")
            return
        
        print(f"Found {len(resume_files)} resume(s) to analyze...")
        
        # Initialize ranker
        ranker = ResumeRanker()
        
        # Rank resumes
        print("\nAnalyzing resumes...")
        results = ranker.rank_resumes(jd_path, resume_files)
        
        # Display results
        print("\nRanked Resumes:")
        print("-" * 50)
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {os.path.basename(result['resume_path'])}")
            print(ranker.get_score_breakdown(result))
            print("-" * 50)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
 