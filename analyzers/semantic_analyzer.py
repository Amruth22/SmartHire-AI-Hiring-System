"""
Semantic Analyzer - Pure Tool
Performs semantic similarity analysis using SBERT
NO state management, NO orchestration logic
"""

import logging
from typing import Dict, Any
from sentence_transformers import SentenceTransformer, util

logger = logging.getLogger("semantic_analyzer")


class SemanticAnalyzer:
    """Pure semantic similarity tool - reusable across workflows"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize semantic analyzer
        
        Args:
            model_name: Name of the sentence transformer model
        """
        try:
            self.model = SentenceTransformer(model_name)
            logger.info(f"Semantic analyzer initialized with model: {model_name}")
        except Exception as e:
            logger.error(f"Failed to load semantic model: {e}")
            self.model = None
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate semantic similarity between two texts
        
        Args:
            text1: First text
            text2: Second text
        
        Returns:
            Similarity score (0.0 to 1.0)
        """
        if not self.model:
            logger.warning("Semantic model not available, returning default similarity")
            return 0.5
        
        try:
            # Encode texts
            embeddings = self.model.encode([text1, text2])
            
            # Calculate cosine similarity
            similarity = util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()
            
            logger.debug(f"Similarity calculated: {similarity:.3f}")
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Similarity calculation failed: {e}")
            return 0.5
    
    def evaluate_concept_answer(self, question: str, reference_answer: str,
                               student_answer: str) -> Dict[str, Any]:
        """
        Evaluate a concept question answer using semantic similarity
        
        Args:
            question: Question text
            reference_answer: Reference answer
            student_answer: Student's answer
        
        Returns:
            Dictionary with score and feedback
        """
        if not self.model:
            return {
                "score": 5.0,
                "feedback": "Semantic evaluation unavailable",
                "similarity": 0.5
            }
        
        try:
            # Calculate similarity
            similarity = self.calculate_similarity(reference_answer, student_answer)
            
            # Convert similarity to score (0-10 scale)
            score = round(similarity * 10, 2)
            
            # Generate feedback based on similarity
            if similarity >= 0.85:
                feedback = "Excellent answer with strong semantic alignment to the reference"
            elif similarity >= 0.70:
                feedback = "Good answer with reasonable semantic similarity"
            elif similarity >= 0.50:
                feedback = "Moderate answer, could be more aligned with expected response"
            else:
                feedback = "Answer needs improvement, low semantic similarity to reference"
            
            logger.info(f"Concept answer evaluated: score={score}, similarity={similarity:.3f}")
            
            return {
                "score": score,
                "feedback": feedback,
                "similarity": similarity,
                "method": "semantic_similarity"
            }
            
        except Exception as e:
            logger.error(f"Concept answer evaluation failed: {e}")
            return {
                "score": 5.0,
                "feedback": f"Evaluation error: {str(e)}",
                "similarity": 0.5
            }
    
    def batch_similarity(self, reference: str, candidates: list) -> list:
        """
        Calculate similarity between reference and multiple candidates
        
        Args:
            reference: Reference text
            candidates: List of candidate texts
        
        Returns:
            List of similarity scores
        """
        if not self.model:
            return [0.5] * len(candidates)
        
        try:
            # Encode all texts
            ref_embedding = self.model.encode(reference)
            candidate_embeddings = self.model.encode(candidates)
            
            # Calculate similarities
            similarities = []
            for candidate_emb in candidate_embeddings:
                sim = util.pytorch_cos_sim(ref_embedding, candidate_emb).item()
                similarities.append(float(sim))
            
            return similarities
            
        except Exception as e:
            logger.error(f"Batch similarity calculation failed: {e}")
            return [0.5] * len(candidates)
    
    def is_available(self) -> bool:
        """Check if semantic analyzer is available"""
        return self.model is not None
