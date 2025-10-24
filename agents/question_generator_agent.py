"""
Question Generator Agent

Agent responsible for coordinating interview question generation.
Uses AIAnalyzer as a tool for question creation.
"""

from typing import Dict, Any, List
from .base_agent import BaseAgent
from analyzers.ai_analyzer import AIAnalyzer


class QuestionGeneratorAgent(BaseAgent):
    """Agent for interview question generation"""
    
    def __init__(self):
        """Initialize question generator agent with AI analyzer"""
        super().__init__("question_generator")
        self.ai_analyzer = AIAnalyzer("GEMINI_API_KEY_3")
        self.log("Question Generator agent initialized")
    
    def analyze(self, experience_level: str, job_title: str,
                resume_features: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate personalized interview questions
        
        Args:
            experience_level: Candidate experience level
            job_title: Job title
            resume_features: Resume features
        
        Returns:
            List of question dictionaries
        """
        self.log(f"Generating questions for {experience_level} {job_title}")
        
        # Use AI analyzer tool for question generation
        questions = self.ai_analyzer.generate_questions(
            experience_level,
            job_title,
            resume_features
        )
        
        self.log(f"Generated {len(questions)} interview questions")
        
        return questions
