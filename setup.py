import subprocess
import sys
import os

def install_requirements():
    """Install required packages."""
    print("Installing required packages...")
    
    # First, ensure pip is up to date
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    
    # Install PyMuPDF separately first
    print("Installing PyMuPDF...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "PyMuPDF"])
    
    # Install other requirements
    print("Installing other requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Install spaCy model
    print("Installing spaCy model...")
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    
    # Create required directories
    print("Creating required directories...")
    os.makedirs("resumes", exist_ok=True)
    os.makedirs("Job_descriptions", exist_ok=True)
    
    print("\nSetup completed successfully!")
    print("\nNext steps:")
    print("1. Place your job description PDF in the 'Job_descriptions' directory")
    print("2. Place the resumes you want to analyze in the 'resumes' directory")
    print("3. Run 'python main.py' to start the analysis")

if __name__ == "__main__":
    install_requirements() 