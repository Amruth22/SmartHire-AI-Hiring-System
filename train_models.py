"""
Training Script for SmartHire ML Models
Run this script to pre-train the models before using the application
"""

import os
import sys
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, r2_score, mean_absolute_error
import joblib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("train_models")


def train_experience_model():
    """Train experience level prediction model"""
    logger.info("Training Experience Level Model...")
    
    try:
        # Load training data
        data_path = "data/experience_level_training_dataset.csv"
        if not os.path.exists(data_path):
            logger.warning(f"Training data not found at {data_path}")
            return False
        
        df = pd.read_csv(data_path)
        
        # Features and target
        feature_cols = [
            'skills_count', 
            'projects_count', 
            'certifications_count',
            'leadership_experience', 
            'has_research_work'
        ]
        
        X = df[feature_cols]
        y = df['experience_level']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Evaluate
        train_acc = accuracy_score(y_train, model.predict(X_train))
        test_acc = accuracy_score(y_test, model.predict(X_test))
        
        logger.info(f"Training accuracy: {train_acc:.3f}")
        logger.info(f"Test accuracy: {test_acc:.3f}")
        
        # Save model
        os.makedirs("models", exist_ok=True)
        model_path = "models/experience_predictor_model.pkl"
        joblib.dump(model, model_path)
        
        logger.info(f"Model saved to {model_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error training experience model: {e}")
        return False


def train_resume_score_model():
    """Train resume quality scoring model"""
    logger.info("Training Resume Score Model...")
    
    try:
        # Load training data
        data_path = "data/resume_score_training_dataset.csv"
        if not os.path.exists(data_path):
            logger.warning(f"Training data not found at {data_path}")
            return False
        
        df = pd.read_csv(data_path)
        
        # Features and target
        feature_cols = [
            'total_experience_years',
            'skills_count',
            'projects_count',
            'certifications_count',
            'education_level'
        ]
        
        X = df[feature_cols]
        y = df['resume_score']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Evaluate
        train_r2 = r2_score(y_train, model.predict(X_train))
        test_r2 = r2_score(y_test, model.predict(X_test))
        test_mae = mean_absolute_error(y_test, model.predict(X_test))
        
        logger.info(f"Training R2 score: {train_r2:.3f}")
        logger.info(f"Test R2 score: {test_r2:.3f}")
        logger.info(f"Test MAE: {test_mae:.3f}")
        
        # Save model
        os.makedirs("models", exist_ok=True)
        model_path = "models/resume_scorer_model.pkl"
        joblib.dump(model, model_path)
        
        logger.info(f"Model saved to {model_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error training resume score model: {e}")
        return False


def main():
    """Train all ML models"""
    
    print("=" * 70)
    print("SMARTHIRE MODEL TRAINING")
    print("=" * 70)
    
    # Create models directory
    os.makedirs("models", exist_ok=True)
    
    # Train experience level model
    print("\n[1/2] Training Experience Level Model...")
    exp_success = train_experience_model()
    if exp_success:
        print("[SUCCESS] Experience Level Model trained successfully")
    else:
        print("[WARNING] Experience Level Model training failed - will use rule-based fallback")
    
    # Train resume score model
    print("\n[2/2] Training Resume Score Model...")
    score_success = train_resume_score_model()
    if score_success:
        print("[SUCCESS] Resume Score Model trained successfully")
    else:
        print("[WARNING] Resume Score Model training failed - will use rule-based fallback")
    
    print("\n" + "=" * 70)
    print("MODEL TRAINING COMPLETED")
    print("=" * 70)
    
    if exp_success and score_success:
        print("\n[SUCCESS] All models trained successfully!")
    else:
        print("\n[WARNING] Some models failed to train - fallback methods will be used")
    
    print("\nNext steps:")
    print("1. Set up your .env file with Gemini API keys")
    print("2. Run: streamlit run main.py")
    print("3. Start evaluating candidates!")


if __name__ == "__main__":
    main()
