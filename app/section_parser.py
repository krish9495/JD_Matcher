import re
from typing import Dict, List, Optional

class SectionParser:
    def __init__(self):
        # Common section headers in resumes
        self.section_patterns = {
            'skills': r'(?i)(?:skills|technical skills|core competencies|expertise|proficiencies?)(?:\s*:|\s*$)',
            'experience': r'(?i)(?:experience|work experience|employment|professional experience|work history)(?:\s*:|\s*$)',
            'education': r'(?i)(?:education|academic|qualification|degree|university)(?:\s*:|\s*$)',
            'projects': r'(?i)(?:projects|portfolio|achievements|accomplishments)(?:\s*:|\s*$)'
        }
        
        # Compile regex patterns
        self.compiled_patterns = {
            section: re.compile(pattern, re.MULTILINE)
            for section, pattern in self.section_patterns.items()
        }

    def find_section_boundaries(self, text: str) -> Dict[str, List[tuple]]:
        """Find the start and end positions of each section in the text."""
        sections = {}
        
        # Find all section headers
        for section, pattern in self.compiled_patterns.items():
            matches = list(pattern.finditer(text))
            if matches:
                sections[section] = []
                for i, match in enumerate(matches):
                    start = match.end()
                    # If this is the last match, end at the end of text
                    if i == len(matches) - 1:
                        end = len(text)
                    else:
                        # End at the start of the next section
                        end = matches[i + 1].start()
                    sections[section].append((start, end))
        
        return sections

    def extract_section_content(self, text: str, start: int, end: int) -> str:
        """Extract and clean section content."""
        content = text[start:end].strip()
        # Remove multiple newlines
        content = re.sub(r'\n\s*\n', '\n', content)
        return content

    def parse_sections(self, text: str) -> Dict[str, List[str]]:
        """Parse text into sections and return a dictionary of section contents."""
        section_boundaries = self.find_section_boundaries(text)
        parsed_sections = {}
        
        for section, boundaries in section_boundaries.items():
            parsed_sections[section] = [
                self.extract_section_content(text, start, end)
                for start, end in boundaries
            ]
        
        # If any section is missing, add an empty list
        for section in self.section_patterns.keys():
            if section not in parsed_sections:
                parsed_sections[section] = []
        
        return parsed_sections

    def get_section_text(self, sections: Dict[str, List[str]], section_name: str) -> str:
        """Get combined text for a specific section."""
        if section_name not in sections:
            return ""
        return "\n".join(sections[section_name]) 