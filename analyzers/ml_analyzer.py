"""
ML Analyzer - Pure Tool
Performs ML-based predictions using trained models
NO state management, NO orchestration logic
"""

import logging
import os
import joblib
import numpy as np
from typing import Dict, Any

logger = logging.getLogger("ml_analyzer")


class MLAnalyzer:
    """Pure ML analysis tool - reusable across workflows"""
    
    def __init__(self):
        """Initialize ML analyzer and load models"""
        self.experience_model = None
        self.resume_scorer_model = None
        self._load_models()
        logger.info("ML Analyzer initialized")
    
    def _load_models(self):
        """Load trained ML models"""
        try:
            # Load experience predictor model
            exp_model_path = "models/experience_predictor_model.pkl"
            if os.path.exists(exp_model_path):
                self.experience_model = joblib.load(exp_model_path)
                logger.info("Experience predictor model loaded")
            else:
                logger.warning(f"Experience model not found at {exp_model_path}")
            
            # Load resume scorer model
            scorer_model_path = "models/resume_scorer_model.pkl"
            if os.path.exists(scorer_model_path):
                self.resume_scorer_model = joblib.load(scorer_model_path)
                logger.info("Resume scorer model loaded")
            else:
                logger.warning(f"Resume scorer model not found at {scorer_model_path}")
                
        except Exception as e:
            logger.error(f"Error loading ML models: {e}")
    
    def predict_experience_level(self, resume_features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict candidate experience level using ML model
        
        Args:
            resume_features: Extracted resume features
        
        Returns:
            Dictionary with experience level and confidence
        """
        try:
            # Extract features for ML model
            features = self._extract_experience_features(resume_features)
            
            if self.experience_model is not None:
                # Use ML model
                feature_array = np.array([list(features.values())])
                prediction = self.experience_model.predict(feature_array)[0]
                
                # Get confidence if available
                confidence = 0.85
                if hasattr(self.experience_model, 'predict_proba'):
                    proba = self.experience_model.predict_proba(feature_array)[0]
                    confidence = float(max(proba))
                
                logger.info(f"ML prediction: {prediction} (confidence: {confidence:.2f})")
                
                return {
                    "experience_level": prediction,
                    "confidence": confidence,
                    "method": "ml_model",
                    "features_used": features
                }
            else:
                # Fallback to rule-based
                return self._rule_based_experience(features)
                
        except Exception as e:
            logger.error(f"Experience prediction failed: {e}")
            return self._rule_based_experience(
                self._extract_experience_features(resume_features)
            )
    
    def score_resume(self, resume_features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Score resume quality using ML model
        
        Args:
            resume_features: Extracted resume features
        
        Returns:
            Dictionary with resume score and breakdown
        """
        try:
            # Extract features for ML model
            features = self._extract_scoring_features(resume_features)
            
            if self.resume_scorer_model is not None:
                # Use ML model
                feature_array = np.array([list(features.values())])
                score = float(self.resume_scorer_model.predict(feature_array)[0])
                score = min(10.0, max(0.0, score))
                
                logger.info(f"ML resume score: {score:.2f}")
                
                return {
                    "resume_score": score,
                    "method": "ml_model",
                    "features_used": features,
                    "score_breakdown": self._calculate_breakdown(features)
                }
            else:
                # Fallback to rule-based
                return self._rule_based_scoring(features)
                
        except Exception as e:
            logger.error(f"Resume scoring failed: {e}")
            return self._rule_based_scoring(
                self._extract_scoring_features(resume_features)
            )
    
    def _extract_experience_features(self, resume_features: Dict[str, Any]) -> Dict[str, float]:
        """Extract features for experience prediction"""
        return {
            "skills_count": float(len(resume_features.get("skills", []))),
            "projects_count": float(len(resume_features.get("projects", []))),
            "certifications_count": float(len(resume_features.get("certifications", []))),
            "leadership_experience": float(resume_features.get("leadership_experience", 0)),
            "has_research_work": float(resume_features.get("has_research_work", 0))
        }
    
    def _extract_scoring_features(self, resume_features: Dict[str, Any]) -> Dict[str, float]:
        """Extract features for resume scoring"""
        return {
            "total_experience_years": float(resume_features.get("total_experience_years", 0)),
            "skills_count": float(len(resume_features.get("skills", []))),
            "projects_count": float(len(resume_features.get("projects", []))),
            "certifications_count": float(len(resume_features.get("certifications", []))),
            "education_level": self._encode_education(resume_features.get("education", {}))
        }
    
    def _encode_education(self, education: Dict[str, Any]) -> float:
        """Encode education level as numeric value"""
        degree = education.get("degree", "").lower()
        
        if "phd" in degree or "doctorate" in degree:
            return 4.0
        elif "master" in degree or "msc" in degree or "mba" in degree:
            return 3.0
        elif "bachelor" in degree or "bsc" in degree or "btech" in degree:
            return 2.0
        elif "associate" in degree or "diploma" in degree:
            return 1.0
        else:
            return 0.0
    
    def _rule_based_experience(self, features: Dict[str, float]) -> Dict[str, Any]:
        """Rule-based experience level prediction"""
        skills = features.get("skills_count", 0)
        projects = features.get("projects_count", 0)
        certs = features.get("certifications_count", 0)
        leadership = features.get("leadership_experience", 0)
        
        # Calculate score
        score = (skills * 0.3) + (projects * 0.3) + (certs * 0.2) + (leadership * 0.2)
        
        if score >= 8 or (skills >= 12 and projects >= 5):
            level = "Senior"
        elif score >= 4 or (skills >= 6 and projects >= 2):
            level = "Mid-Level"
        else:
            level = "Junior"
        
        logger.info(f"Rule-based prediction: {level}")
        
        return {
            "experience_level": level,
            "confidence": 0.7,
            "method": "rule_based",
            "features_used": features
        }
    
    def _rule_based_scoring(self, features: Dict[str, float]) -> Dict[str, Any]:
        """Rule-based resume scoring"""
        exp_years = features.get("total_experience_years", 0)
        skills = features.get("skills_count", 0)
        projects = features.get("projects_count", 0)
        certs = features.get("certifications_count", 0)
        education = features.get("education_level", 0)
        
        # Calculate weighted score
        score = (
            min(exp_years * 0.5, 3.0) +  # Max 3 points for experience
            min(skills * 0.2, 2.5) +      # Max 2.5 points for skills
            min(projects * 0.3, 2.0) +    # Max 2 points for projects
            min(certs * 0.4, 1.5) +       # Max 1.5 points for certs
            education * 0.25              # Max 1 point for education
        )
        
        score = min(10.0, max(0.0, score))
        
        logger.info(f"Rule-based score: {score:.2f}")
        
        return {
            "resume_score": score,
            "method": "rule_based",
            "features_used": features,
            "score_breakdown": self._calculate_breakdown(features)
        }
    
    def _calculate_breakdown(self, features: Dict[str, float]) -> Dict[str, float]:
        """Calculate score breakdown by component"""
        return {
            "experience_score": min(10.0, features.get("total_experience_years", 0) * 1.5),
            "skills_score": min(10.0, features.get("skills_count", 0) * 0.8),
            "projects_score": min(10.0, features.get("projects_count", 0) * 1.5),
            "certifications_score": min(10.0, features.get("certifications_count", 0) * 2.0),
            "education_score": features.get("education_level", 0) * 2.5
        }
