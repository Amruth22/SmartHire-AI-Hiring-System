"""
Job Fit Analyzer Agent

Agent responsible for coordinating job fit analysis.
Uses AIAnalyzer as a tool for compatibility assessment.
"""

from typing import Dict, Any
from .base_agent import BaseAgent
from analyzers.ai_analyzer import AIAnalyzer


class JobFitAnalyzerAgent(BaseAgent):
    """Agent for job fit analysis"""
    
    def __init__(self):
        """Initialize job fit analyzer agent with AI analyzer"""
        super().__init__("job_fit_analyzer")
        self.ai_analyzer = AIAnalyzer("GEMINI_API_KEY_2")
        self.log("Job Fit Analyzer agent initialized")
    
    def analyze(self, resume_features: Dict[str, Any], 
                job_description: str, job_title: str) -> Dict[str, Any]:
        """
        Analyze job fit between candidate and position
        
        Args:
            resume_features: Extracted resume features
            job_description: Job description text
            job_title: Job title
        
        Returns:
            Dictionary with job fit analysis
        """
        self.log(f"Starting job fit analysis for {job_title}")
        
        # Use AI analyzer tool for job fit analysis
        results = self.ai_analyzer.analyze_job_fit(
            resume_features, 
            job_description, 
            job_title
        )
        
        fit_level = results.get("job_fit", "Moderate Fit")
        fit_score = results.get("fit_score", 6.0)
        
        self.log(f"Job fit analyzed: {fit_level} (score: {fit_score:.1f}/10)")
        
        return results
