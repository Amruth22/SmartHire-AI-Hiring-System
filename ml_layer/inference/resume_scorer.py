"""
Resume Score Predictor - Inference Module

Predicts resume quality score (0-10) using trained ML model.
"""

import joblib
import os
import logging
from typing import Dict, Any

logger = logging.getLogger("ml_layer.inference.resume_scorer")


class ResumeScorer:
    """Predicts resume score using trained ML model"""
    
    def __init__(self):
        """Initialize scorer"""
        self.model_dir = "ml_layer/models"
        self.model_path = os.path.join(self.model_dir, "resume_score_model.pkl")
        self.scaler_path = os.path.join(self.model_dir, "resume_score_scaler.pkl")
        self.features_path = os.path.join(self.model_dir, "resume_score_features.pkl")
        
        self.model = None
        self.scaler = None
        self.features = None
        self._loaded = False
    
    def load_model(self):
        """Load trained model and metadata"""
        if self._loaded:
            return True
        
        try:
            if not os.path.exists(self.model_path):
                logger.warning(f"Model not found at {self.model_path}")
                return False
            
            if not os.path.exists(self.scaler_path):
                logger.warning(f"Scaler not found at {self.scaler_path}")
                return False
            
            if not os.path.exists(self.features_path):
                logger.warning(f"Features not found at {self.features_path}")
                return False
            
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
            self.features = joblib.load(self.features_path)
            
            self._loaded = True
            logger.info("Resume scorer model loaded successfully")
            logger.info(f"Features: {self.features}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False
    
    def predict(self, resume_features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict resume score
        
        Args:
            resume_features: Dictionary with resume features
        
        Returns:
            Dictionary with prediction results
        """
        # Try to load model if not loaded
        if not self._loaded:
            if not self.load_model():
                return self._fallback_scoring(resume_features)
        
        try:
            # Prepare input features
            ml_input = {}
            
            if 'total_experience_years' in self.features:
                ml_input['total_experience_years'] = float(
                    resume_features.get("total_experience_years", 0)
                )
            
            if 'skills_count' in self.features:
                skills = resume_features.get("skills", [])
                ml_input['skills_count'] = len(skills) if isinstance(skills, list) else 0
            
            if 'project_count' in self.features:
                projects = resume_features.get("projects", [])
                ml_input['project_count'] = len(projects) if isinstance(projects, list) else 0
            
            if 'certification_count' in self.features:
                certs = resume_features.get("certifications", [])
                ml_input['certification_count'] = len(certs) if isinstance(certs, list) else 0
            
            if 'leadership_experience' in self.features:
                ml_input['leadership_experience'] = int(
                    resume_features.get("leadership_experience", 0)
                )
            
            if 'has_research_work' in self.features:
                ml_input['has_research_work'] = int(
                    resume_features.get("has_research_work", 0)
                )
            
            # Create feature vector in correct order
            feature_vector = [[ml_input.get(feat, 0) for feat in self.features]]
            
            # Scale and predict
            feature_vector_scaled = self.scaler.transform(feature_vector)
            prediction = self.model.predict(feature_vector_scaled)[0]
            
            # Ensure score is between 0 and 10
            prediction = max(0.0, min(10.0, float(prediction)))
            
            logger.info(f"ML Resume Score: {prediction:.2f}/10")
            
            # Calculate breakdown (approximate based on feature importance)
            breakdown = self._calculate_breakdown(ml_input, prediction)
            
            return {
                "resume_score": prediction,
                "method": "ml_model",
                "breakdown": breakdown,
                "features_used": ml_input
            }
            
        except Exception as e:
            logger.error(f"Scoring error: {e}")
            return self._fallback_scoring(resume_features)
    
    def _calculate_breakdown(self, ml_input: Dict[str, float], total_score: float) -> Dict[str, float]:
        """
        Calculate score breakdown by component
        
        Args:
            ml_input: Input features
            total_score: Total predicted score
        
        Returns:
            Dictionary with score breakdown
        """
        # Approximate weights based on typical feature importance
        weights = {
            'total_experience_years': 0.30,
            'skills_count': 0.25,
            'project_count': 0.20,
            'certification_count': 0.15,
            'leadership_experience': 0.05,
            'has_research_work': 0.05
        }
        
        breakdown = {}
        for feature, weight in weights.items():
            if feature in ml_input:
                # Normalize feature value to 0-10 scale
                if feature == 'total_experience_years':
                    normalized = min(10, ml_input[feature] * 1.5)
                elif feature == 'skills_count':
                    normalized = min(10, ml_input[feature] * 0.5)
                elif feature == 'project_count':
                    normalized = min(10, ml_input[feature] * 1.0)
                elif feature == 'certification_count':
                    normalized = min(10, ml_input[feature] * 2.0)
                else:
                    normalized = ml_input[feature] * 10
                
                breakdown[feature] = round(normalized, 2)
        
        return breakdown
    
    def _fallback_scoring(self, resume_features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fallback rule-based scoring
        
        Args:
            resume_features: Dictionary with resume features
        
        Returns:
            Dictionary with scoring results
        """
        logger.info("Using rule-based fallback for resume scoring")
        
        exp_years = float(resume_features.get("total_experience_years", 0))
        skills = resume_features.get("skills", [])
        skills_count = len(skills) if isinstance(skills, list) else 0
        projects = resume_features.get("projects", [])
        project_count = len(projects) if isinstance(projects, list) else 0
        certs = resume_features.get("certifications", [])
        cert_count = len(certs) if isinstance(certs, list) else 0
        leadership = int(resume_features.get("leadership_experience", 0))
        research = int(resume_features.get("has_research_work", 0))
        
        # Rule-based scoring
        score = 0.0
        
        # Experience points (0-3)
        exp_score = min(3.0, exp_years * 0.5)
        score += exp_score
        
        # Skills points (0-2.5)
        skills_score = min(2.5, skills_count * 0.2)
        score += skills_score
        
        # Projects points (0-2)
        projects_score = min(2.0, project_count * 0.5)
        score += projects_score
        
        # Certifications points (0-1.5)
        cert_score = min(1.5, cert_count * 0.4)
        score += cert_score
        
        # Leadership points (0-0.5)
        leadership_score = 0.5 if leadership else 0.0
        score += leadership_score
        
        # Research points (0-0.5)
        research_score = 0.5 if research else 0.0
        score += research_score
        
        # Ensure score is between 0 and 10
        score = max(0.0, min(10.0, score))
        
        logger.info(f"Rule-based score: {score:.2f}/10")
        
        breakdown = {
            "experience": round(exp_score * (10/3), 2),
            "skills": round(skills_score * (10/2.5), 2),
            "projects": round(projects_score * (10/2), 2),
            "certifications": round(cert_score * (10/1.5), 2),
            "leadership": round(leadership_score * 10, 2),
            "research": round(research_score * 10, 2)
        }
        
        return {
            "resume_score": round(score, 2),
            "method": "rule_based",
            "breakdown": breakdown,
            "reasoning": f"Based on {exp_years}y exp, {skills_count} skills, {project_count} projects, {cert_count} certs"
        }
    
    def is_available(self) -> bool:
        """Check if ML model is available"""
        return self._loaded or self.load_model()


# Global scorer instance
_scorer = None


def get_scorer() -> ResumeScorer:
    """Get global scorer instance"""
    global _scorer
    if _scorer is None:
        _scorer = ResumeScorer()
    return _scorer


def score_resume(resume_features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function to score resume
    
    Args:
        resume_features: Dictionary with resume features
    
    Returns:
        Dictionary with scoring results
    """
    scorer = get_scorer()
    return scorer.predict(resume_features)
