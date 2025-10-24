"""
Resume Scorer Agent

Agent responsible for coordinating resume quality scoring.
Uses MLAnalyzer as a tool for scoring.
"""

from typing import Dict, Any
from .base_agent import BaseAgent
from analyzers.ml_analyzer import MLAnalyzer


class ResumeScorerAgent(BaseAgent):
    """Agent for resume quality scoring"""
    
    def __init__(self):
        """Initialize resume scorer agent with ML analyzer"""
        super().__init__("resume_scorer")
        self.ml_analyzer = MLAnalyzer()
        self.log("Resume Scorer agent initialized")
    
    def analyze(self, resume_features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Score resume quality
        
        Args:
            resume_features: Extracted resume features
        
        Returns:
            Dictionary with resume score and breakdown
        """
        self.log("Starting resume quality scoring")
        
        # Use ML analyzer tool for scoring
        results = self.ml_analyzer.score_resume(resume_features)
        
        score = results.get("resume_score", 5.0)
        method = results.get("method", "unknown")
        
        self.log(f"Resume scored: {score:.2f}/10 (method: {method})")
        
        return results
