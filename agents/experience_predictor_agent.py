"""
Experience Predictor Agent

Agent responsible for coordinating experience level prediction.
Uses AIAnalyzer (Gemini AI) for all predictions.
"""

from typing import Dict, Any
from .base_agent import BaseAgent
from analyzers.ai_analyzer import AIAnalyzer


class ExperiencePredictorAgent(BaseAgent):
    """Agent for experience level prediction"""

    def __init__(self):
        """Initialize experience predictor agent with AI analyzer"""
        super().__init__("experience_predictor")
        self.ai_analyzer = AIAnalyzer("GEMINI_API_KEY_2")
        self.log("Experience Predictor agent initialized")

    def analyze(self, resume_features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict candidate experience level

        Args:
            resume_features: Extracted resume features

        Returns:
            Dictionary with experience level and prediction details
        """
        self.log("Starting experience level prediction")

        # Use AI analyzer tool for prediction
        results = self.ai_analyzer.predict_experience_level(resume_features)

        experience_level = results.get("experience_level", "Mid-Level")
        confidence = results.get("confidence", 0.7)

        self.log(f"Experience predicted: {experience_level} (confidence: {confidence:.2f})")

        return results
