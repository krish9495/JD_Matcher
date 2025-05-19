try:
    import fitz
    from fitz import open as fitz_open
except ImportError:
    raise ImportError("PyMuPDF (fitz) is not installed. Please run 'pip install PyMuPDF'")

import docx
import os

def extract_text_from_pdf(path):
    """Extract text from PDF file with error handling."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"PDF file not found: {path}")
    try:
        with fitz_open(path) as doc:
            text = []
            for page in doc:
                text.append(page.get_text())
            return "\n".join(text)
    except Exception as e:
        raise Exception(f"Error extracting text from PDF {path}: {str(e)}")

def extract_text_from_docx(path):
    """Extract text from DOCX file with error handling."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"DOCX file not found: {path}")
    try:
        doc = docx.Document(path)
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        raise Exception(f"Error extracting text from DOCX {path}: {str(e)}")

def extract_text(path):
    """Extract text from various file formats with error handling."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
        
    if path.endswith(".pdf"):
        return extract_text_from_pdf(path)
    elif path.endswith(".docx"):
        return extract_text_from_docx(path)
    elif path.endswith(".txt"):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise Exception(f"Error reading text file {path}: {str(e)}")
    else:
        raise ValueError(f"Unsupported file format: {path}") 