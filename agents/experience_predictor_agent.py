"""
Experience Predictor Agent

Agent responsible for coordinating experience level prediction.
Uses MLAnalyzer as primary tool, AIAnalyzer as fallback.
"""

from typing import Dict, Any
from .base_agent import BaseAgent
from analyzers.ml_analyzer import MLAnalyzer
from analyzers.ai_analyzer import AIAnalyzer


class ExperiencePredictorAgent(BaseAgent):
    """Agent for experience level prediction"""
    
    def __init__(self):
        """Initialize experience predictor agent with analyzers"""
        super().__init__("experience_predictor")
        self.ml_analyzer = MLAnalyzer()
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
        
        # Use ML analyzer tool for prediction
        results = self.ml_analyzer.predict_experience_level(resume_features)
        
        experience_level = results.get("experience_level", "Mid-Level")
        confidence = results.get("confidence", 0.7)
        method = results.get("method", "unknown")
        
        self.log(f"Experience predicted: {experience_level} (confidence: {confidence:.2f}, method: {method})")
        
        return results
