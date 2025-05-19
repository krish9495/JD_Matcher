import spacy
import numpy as np
from sentence_transformers import SentenceTransformer
from keybert import KeyBERT
from typing import Dict, List, Tuple
import pandas as pd
from .text_extractor import extract_text
from .section_parser import SectionParser

class ResumeRanker:
    def __init__(self):
        # Initialize models
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.keyword_model = KeyBERT()
        self.nlp = spacy.load("en_core_web_sm")
        self.section_parser = SectionParser()
        
        # Section weights
        self.section_weights = {
            'skills': 0.4,
            'experience': 0.3,
            'education': 0.2,
            'projects': 0.1
        }

    def extract_keywords(self, text: str, top_n: int = 10) -> List[str]:
        """Extract keywords from text using KeyBERT."""
        keywords = self.keyword_model.extract_keywords(text, 
                                                     keyphrase_ngram_range=(1, 2),
                                                     stop_words='english',
                                                     top_n=top_n)
        return [keyword for keyword, score in keywords]

    def get_section_embeddings(self, text: str) -> Dict[str, np.ndarray]:
        """Extract and embed different sections of the resume."""
        sections = self.section_parser.parse_sections(text)
        embeddings = {}
        
        for section, content_list in sections.items():
            section_text = self.section_parser.get_section_text(sections, section)
            if section_text:
                embeddings[section] = self.embedding_model.encode(section_text)
            else:
                # Use empty embedding if section is not found
                embeddings[section] = np.zeros(384)  # 384 is the dimension of all-MiniLM-L6-v2
        
        return embeddings

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities from text using spaCy."""
        doc = self.nlp(text)
        entities = {
            'SKILL': [],
            'ORG': [],
            'WORK_OF_ART': [],
            'PERSON': []
        }
        
        for ent in doc.ents:
            if ent.label_ in entities:
                entities[ent.label_].append(ent.text)
        
        return entities

    def calculate_section_similarity(self, 
                                  resume_section: str, 
                                  jd_section: str) -> float:
        """Calculate cosine similarity between resume and JD sections."""
        resume_embedding = self.embedding_model.encode(resume_section)
        jd_embedding = self.embedding_model.encode(jd_section)
        
        similarity = np.dot(resume_embedding, jd_embedding) / (
            np.linalg.norm(resume_embedding) * np.linalg.norm(jd_embedding)
        )
        return float(similarity)

    def rank_resumes(self, 
                    jd_path: str, 
                    resume_paths: List[str]) -> List[Dict]:
        """Rank resumes based on multiple criteria."""
        # Extract JD text
        jd_text = extract_text(jd_path)
        jd_sections = self.section_parser.parse_sections(jd_text)
        jd_keywords = self.extract_keywords(jd_text)
        jd_entities = self.extract_entities(jd_text)
        
        results = []
        
        for resume_path in resume_paths:
            resume_text = extract_text(resume_path)
            resume_sections = self.section_parser.parse_sections(resume_text)
            resume_entities = self.extract_entities(resume_text)
            
            # Calculate section similarities
            section_scores = {}
            for section, weight in self.section_weights.items():
                resume_section_text = self.section_parser.get_section_text(resume_sections, section)
                jd_section_text = self.section_parser.get_section_text(jd_sections, section)
                
                if resume_section_text and jd_section_text:
                    section_scores[section] = self.calculate_section_similarity(
                        resume_section_text, jd_section_text
                    )
                else:
                    section_scores[section] = 0.0
            
            # Calculate keyword match score
            resume_keywords = self.extract_keywords(resume_text)
            keyword_match = len(set(resume_keywords) & set(jd_keywords)) / len(jd_keywords)
            
            # Calculate total score
            total_score = sum(score * weight for score, weight in zip(
                section_scores.values(), self.section_weights.values()
            ))
            
            results.append({
                'resume_path': resume_path,
                'section_scores': section_scores,
                'keyword_match': keyword_match,
                'total_score': total_score,
                'entities': resume_entities,
                'sections': resume_sections
            })
        
        # Sort results by total score
        results.sort(key=lambda x: x['total_score'], reverse=True)
        return results

    def get_score_breakdown(self, result: Dict) -> str:
        """Format score breakdown for a single resume."""
        breakdown = []
        for section, score in result['section_scores'].items():
            breakdown.append(f"{section.title()} Match: {score:.1%}")
        breakdown.append(f"Keyword Match: {result['keyword_match']:.1%}")
        breakdown.append(f"Total Score: {result['total_score']:.1%}")
        return "\n".join(breakdown) 