"""
Train All ML Models

Main script to train all machine learning models for SmartHire.
Run this before using the application to pre-train models.
"""

import os
import sys
import logging
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from ml_layer.training.experience_classifier_trainer import train_experience_model
from ml_layer.training.resume_scorer_trainer import train_resume_score_model


def setup_logging():
    """Setup logging configuration"""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"ml_training_{timestamp}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return log_file


def main():
    """Train all ML models"""
    
    print("\n" + "=" * 70)
    print("🚀 SMARTHIRE ML MODEL TRAINING")
    print("=" * 70)
    
    # Setup logging
    log_file = setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting ML model training pipeline")
    logger.info(f"Log file: {log_file}")
    
    # Create models directory
    os.makedirs("ml_layer/models", exist_ok=True)
    logger.info("Models directory created/verified")
    
    results = {}
    
    # Train Experience Level Model
    print("\n" + "-" * 70)
    print("1️⃣  TRAINING EXPERIENCE LEVEL CLASSIFIER")
    print("-" * 70)
    
    try:
        success = train_experience_model()
        results['experience_classifier'] = success
        
        if success:
            print("✅ Experience Level Model trained successfully!")
            logger.info("Experience Level Model training completed successfully")
        else:
            print("❌ Experience Level Model training failed!")
            logger.error("Experience Level Model training failed")
    except Exception as e:
        print(f"❌ Error training Experience Level Model: {e}")
        logger.error(f"Experience Level Model training error: {e}", exc_info=True)
        results['experience_classifier'] = False
    
    # Train Resume Score Model
    print("\n" + "-" * 70)
    print("2️⃣  TRAINING RESUME SCORE PREDICTOR")
    print("-" * 70)
    
    try:
        success = train_resume_score_model()
        results['resume_scorer'] = success
        
        if success:
            print("✅ Resume Score Model trained successfully!")
            logger.info("Resume Score Model training completed successfully")
        else:
            print("❌ Resume Score Model training failed!")
            logger.error("Resume Score Model training failed")
    except Exception as e:
        print(f"❌ Error training Resume Score Model: {e}")
        logger.error(f"Resume Score Model training error: {e}", exc_info=True)
        results['resume_scorer'] = False
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TRAINING SUMMARY")
    print("=" * 70)
    
    total_models = len(results)
    successful = sum(results.values())
    failed = total_models - successful
    
    print(f"\nTotal Models: {total_models}")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    
    print("\nModel Status:")
    for model_name, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"  {model_name}: {status}")
    
    # Check if models exist
    print("\n" + "-" * 70)
    print("📁 MODEL FILES")
    print("-" * 70)
    
    model_files = [
        "ml_layer/models/experience_level_model.pkl",
        "ml_layer/models/experience_level_encoder.pkl",
        "ml_layer/models/experience_features.pkl",
        "ml_layer/models/resume_score_model.pkl",
        "ml_layer/models/resume_score_scaler.pkl",
        "ml_layer/models/resume_score_features.pkl"
    ]
    
    for model_file in model_files:
        exists = os.path.exists(model_file)
        status = "✅ EXISTS" if exists else "❌ MISSING"
        print(f"  {model_file}: {status}")
    
    # Next steps
    print("\n" + "=" * 70)
    print("📋 NEXT STEPS")
    print("=" * 70)
    
    if all(results.values()):
        print("\n✅ All models trained successfully!")
        print("\n1. Set up your .env file with Gemini API keys")
        print("2. Run: streamlit run main.py")
        print("3. Start evaluating candidates!")
        logger.info("All models trained successfully")
    else:
        print("\n⚠️  Some models failed to train")
        print("\n1. Check the log file for details: " + log_file)
        print("2. Verify training data exists in data/ directory")
        print("3. Check for any error messages above")
        logger.warning("Some models failed to train")
    
    print("\n" + "=" * 70)
    
    return all(results.values())


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
