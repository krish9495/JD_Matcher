from app.resume_ranker import ResumeRanker
from app.text_extractor import extract_text

def main():
    # Initialize the ranker
    ranker = ResumeRanker()

    # Example usage
    jd_path = "Job_descriptions/job_description.pdf"  # Update with your JD path
    resume_paths = [
        "resumes/resume1.pdf",  # Update with your resume paths
        "resumes/resume2.pdf"
    ]

    # Rank resumes
    results = ranker.rank_resumes(jd_path, resume_paths)

    # Get detailed breakdown for each resume
    for result in results:
        print(f"\nResume: {result['resume_path']}")
        print(ranker.get_score_breakdown(result))

if __name__ == "__main__":
    main()
