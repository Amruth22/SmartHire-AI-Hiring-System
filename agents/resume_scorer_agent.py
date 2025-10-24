"""
Resume Scorer Agent

Agent responsible for coordinating resume quality scoring.
Uses AIAnalyzer (Gemini AI) for scoring.
"""

from typing import Dict, Any
from .base_agent import BaseAgent
from analyzers.ai_analyzer import AIAnalyzer


class ResumeScorerAgent(BaseAgent):
    """Agent for resume quality scoring"""

    def __init__(self):
        """Initialize resume scorer agent with AI analyzer"""
        super().__init__("resume_scorer")
        self.ai_analyzer = AIAnalyzer("GEMINI_API_KEY_2")
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

        # Use AI analyzer tool for scoring
        results = self.ai_analyzer.score_resume(resume_features)

        score = results.get("resume_score", 5.0)

        self.log(f"Resume scored: {score:.2f}/10")

        return results
