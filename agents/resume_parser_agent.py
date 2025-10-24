"""
Resume Parser Agent

Agent responsible for coordinating resume parsing.
Uses AIAnalyzer as a tool for feature extraction.
"""

from typing import Dict, Any
from .base_agent import BaseAgent
from analyzers.ai_analyzer import AIAnalyzer


class ResumeParserAgent(BaseAgent):
    """Agent for resume parsing and feature extraction"""
    
    def __init__(self):
        """Initialize resume parser agent with AI analyzer"""
        super().__init__("resume_parser")
        self.ai_analyzer = AIAnalyzer("GEMINI_API_KEY_1")
        self.log("Resume Parser agent initialized")
    
    def analyze(self, resume_text: str) -> Dict[str, Any]:
        """
        Parse resume and extract structured features
        
        Args:
            resume_text: Raw resume text
        
        Returns:
            Dictionary with extracted resume features
        """
        self.log("Starting resume parsing")
        
        # Use AI analyzer tool for actual parsing
        features = self.ai_analyzer.parse_resume(resume_text)
        
        candidate_name = features.get("full_name", "Unknown")
        skills_count = len(features.get("skills", []))
        
        self.log(f"Resume parsed successfully for {candidate_name} ({skills_count} skills found)")
        
        return features
