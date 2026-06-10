"""
NLP Service — local text analysis using spaCy.
Zero API calls, completely free, runs offline.

Used for:
- Keyword extraction from answers
- Skill matching between answer and job requirements
- Grammar and communication quality scoring
- Sentence similarity (semantic matching)
"""
import re
from typing import List, Optional

try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
    SPACY_AVAILABLE = True
except (ImportError, OSError):
    SPACY_AVAILABLE = False
    nlp = None


class NLPService:
    """
    Local NLP analysis using spaCy.
    Falls back gracefully if spaCy is not installed.
    """

    def extract_keywords(self, text: str) -> List[str]:
        """
        Extract meaningful keywords from text.
        Returns nouns, proper nouns, and technical terms.
        """
        if not SPACY_AVAILABLE or not nlp:
            return self._simple_keyword_extract(text)

        doc = nlp(text.lower())
        keywords = []
        for token in doc:
            if (
                token.pos_ in ["NOUN", "PROPN"]
                and not token.is_stop
                and len(token.text) > 2
            ):
                keywords.append(token.lemma_)
        return list(set(keywords))

    def calculate_skill_coverage(
        self,
        answer_text: str,
        required_skills: List[str]
    ) -> float:
        """
        Calculate what percentage of required skills are
        mentioned in the candidate's answer.

        Returns float 0.0 to 1.0.
        """
        if not required_skills:
            return 0.0

        answer_lower = answer_text.lower()
        mentioned = 0

        for skill in required_skills:
            if skill.lower() in answer_lower:
                mentioned += 1

        return mentioned / len(required_skills)

    def count_sentences(self, text: str) -> int:
        """Count number of sentences in text."""
        if SPACY_AVAILABLE and nlp:
            doc = nlp(text)
            return len(list(doc.sents))
        # Fallback: count sentence-ending punctuation
        return len(re.findall(r'[.!?]+', text))

    def get_answer_quality_score(self, answer_text: str) -> dict:
        """
        Analyze answer quality based on:
        - Word count (length)
        - Sentence count (structure)
        - Average sentence length (clarity)
        - Vocabulary diversity (lexical richness)

        Returns a dict with quality metrics.
        """
        words = answer_text.strip().split()
        word_count = len(words)
        sentence_count = max(1, self.count_sentences(answer_text))
        avg_sentence_length = word_count / sentence_count
        unique_words = len(set(w.lower() for w in words))
        vocabulary_diversity = (
            unique_words / word_count if word_count > 0 else 0
        )

        # Score based on word count
        if word_count < 20:
            length_score = 30
        elif word_count < 50:
            length_score = 55
        elif word_count < 100:
            length_score = 72
        elif word_count < 200:
            length_score = 82
        else:
            length_score = 88

        # Bonus for structure
        structure_bonus = 5 if sentence_count >= 3 else 0

        # Bonus for vocabulary
        vocab_bonus = 5 if vocabulary_diversity > 0.7 else 0

        total_score = min(100, length_score + structure_bonus + vocab_bonus)

        return {
            "score": total_score,
            "word_count": word_count,
            "sentence_count": sentence_count,
            "avg_sentence_length": round(avg_sentence_length, 1),
            "vocabulary_diversity": round(vocabulary_diversity, 2),
            "keywords": self.extract_keywords(answer_text)
        }

    def extract_skills_from_text(
        self,
        text: str,
        known_skills: Optional[List[str]] = None
    ) -> List[str]:
        """
        Extract technology/skill mentions from text.
        Used for resume parsing and answer analysis.
        """
        # Common tech skills to look for
        tech_skills = [
            "python", "javascript", "typescript", "react", "vue",
            "angular", "fastapi", "django", "flask", "nodejs",
            "postgresql", "mysql", "mongodb", "redis", "docker",
            "kubernetes", "aws", "gcp", "azure", "git", "github",
            "sql", "html", "css", "tailwind", "bootstrap",
            "machine learning", "deep learning", "nlp", "tensorflow",
            "pytorch", "scikit-learn", "pandas", "numpy",
            "rest api", "graphql", "microservices", "agile", "scrum",
        ]

        if known_skills:
            tech_skills.extend([s.lower() for s in known_skills])

        text_lower = text.lower()
        found_skills = []
        for skill in tech_skills:
            if skill in text_lower:
                found_skills.append(skill)

        return list(set(found_skills))

    def _simple_keyword_extract(self, text: str) -> List[str]:
        """Fallback keyword extraction without spaCy."""
        # Remove common stop words
        stop_words = {
            "i", "me", "my", "we", "our", "you", "your", "he",
            "she", "it", "they", "them", "is", "are", "was",
            "were", "be", "been", "have", "has", "had", "do",
            "did", "will", "would", "could", "should", "may",
            "might", "must", "can", "the", "a", "an", "and",
            "or", "but", "in", "on", "at", "to", "for", "of",
            "with", "by", "from", "this", "that", "these",
            "those", "also", "very", "so", "just", "not"
        }
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        return list(set(
            w for w in words if w not in stop_words
        ))

    def is_available(self) -> bool:
        """Check if spaCy is available."""
        return SPACY_AVAILABLE


# Singleton instance
nlp_service = NLPService()
