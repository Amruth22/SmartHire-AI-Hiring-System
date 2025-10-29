"""
Experience Level Predictor - Inference Module

Predicts candidate experience level (Junior/Mid-Level/Senior) using trained ML model.
"""

import joblib
import os
import logging
from typing import Dict, Any

logger = logging.getLogger("ml_layer.inference.experience_predictor")


class ExperiencePredictor:
    """Predicts experience level using trained ML model"""
    
    def __init__(self):
        """Initialize predictor"""
        self.model_dir = "ml_layer/models"
        self.model_path = os.path.join(self.model_dir, "experience_level_model.pkl")
        self.encoder_path = os.path.join(self.model_dir, "experience_level_encoder.pkl")
        self.features_path = os.path.join(self.model_dir, "experience_features.pkl")
        
        self.model = None
        self.encoder = None
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
            
            if not os.path.exists(self.encoder_path):
                logger.warning(f"Encoder not found at {self.encoder_path}")
                return False
            
            if not os.path.exists(self.features_path):
                logger.warning(f"Features not found at {self.features_path}")
                return False
            
            self.model = joblib.load(self.model_path)
            self.encoder = joblib.load(self.encoder_path)
            self.features = joblib.load(self.features_path)
            
            self._loaded = True
            logger.info("Experience predictor model loaded successfully")
            logger.info(f"Features: {self.features}")
            logger.info(f"Classes: {list(self.encoder.classes_)}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False
    
    def predict(self, resume_features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict experience level
        
        Args:
            resume_features: Dictionary with resume features
        
        Returns:
            Dictionary with prediction results
        """
        # Try to load model if not loaded
        if not self._loaded:
            if not self.load_model():
                return self._fallback_prediction(resume_features)
        
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
            
            if 'leadership_experience' in self.features:
                ml_input['leadership_experience'] = int(
                    resume_features.get("leadership_experience", 0)
                )
            
            # Create feature vector in correct order
            feature_vector = [[ml_input.get(feat, 0) for feat in self.features]]
            
            # Predict
            prediction_encoded = self.model.predict(feature_vector)[0]
            prediction = self.encoder.inverse_transform([prediction_encoded])[0]
            
            # Get prediction probabilities
            probabilities = self.model.predict_proba(feature_vector)[0]
            confidence = float(max(probabilities))
            
            logger.info(f"ML Prediction: {prediction} (confidence: {confidence:.2f})")
            
            return {
                "experience_level": prediction,
                "confidence": confidence,
                "method": "ml_model",
                "probabilities": {
                    cls: float(prob) 
                    for cls, prob in zip(self.encoder.classes_, probabilities)
                }
            }
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return self._fallback_prediction(resume_features)
    
    def _fallback_prediction(self, resume_features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fallback rule-based prediction
        
        Args:
            resume_features: Dictionary with resume features
        
        Returns:
            Dictionary with prediction results
        """
        logger.info("Using rule-based fallback for experience prediction")
        
        exp_years = float(resume_features.get("total_experience_years", 0))
        skills = resume_features.get("skills", [])
        skills_count = len(skills) if isinstance(skills, list) else 0
        projects = resume_features.get("projects", [])
        project_count = len(projects) if isinstance(projects, list) else 0
        
        # Rule-based classification
        if exp_years >= 5 or (skills_count >= 12 and project_count >= 5):
            prediction = "Senior"
            confidence = 0.7
        elif exp_years >= 2 or (skills_count >= 6 and project_count >= 2):
            prediction = "Mid-Level"
            confidence = 0.7
        else:
            prediction = "Junior"
            confidence = 0.7
        
        logger.info(f"Rule-based prediction: {prediction}")
        
        return {
            "experience_level": prediction,
            "confidence": confidence,
            "method": "rule_based",
            "reasoning": f"Based on {exp_years} years experience, {skills_count} skills, {project_count} projects"
        }
    
    def is_available(self) -> bool:
        """Check if ML model is available"""
        return self._loaded or self.load_model()


# Global predictor instance
_predictor = None


def get_predictor() -> ExperiencePredictor:
    """Get global predictor instance"""
    global _predictor
    if _predictor is None:
        _predictor = ExperiencePredictor()
    return _predictor


def predict_experience_level(resume_features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function to predict experience level
    
    Args:
        resume_features: Dictionary with resume features
    
    Returns:
        Dictionary with prediction results
    """
    predictor = get_predictor()
    return predictor.predict(resume_features)
