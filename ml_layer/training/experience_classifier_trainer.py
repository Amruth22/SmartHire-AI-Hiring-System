"""
Experience Level Classifier Trainer

Trains a RandomForestClassifier to predict candidate experience level
(Junior, Mid-Level, Senior) based on resume features.
"""

import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import logging

logger = logging.getLogger("ml_layer.training.experience_classifier")


class ExperienceClassifierTrainer:
    """Trains experience level classification model"""
    
    def __init__(self, dataset_path="data/experience_level_training_dataset.csv"):
        """
        Initialize trainer
        
        Args:
            dataset_path: Path to training dataset CSV
        """
        self.dataset_path = dataset_path
        self.model_dir = "ml_layer/models"
        self.model_path = os.path.join(self.model_dir, "experience_level_model.pkl")
        self.encoder_path = os.path.join(self.model_dir, "experience_level_encoder.pkl")
        self.features_path = os.path.join(self.model_dir, "experience_features.pkl")
        
        self.required_features = [
            'total_experience_years',
            'skills_count',
            'project_count',
            'leadership_experience'
        ]
    
    def load_data(self):
        """Load and validate training data"""
        if not os.path.exists(self.dataset_path):
            raise FileNotFoundError(f"Dataset not found at {self.dataset_path}")
        
        df = pd.read_csv(self.dataset_path)
        
        if df.empty:
            raise ValueError("Dataset is empty")
        
        logger.info(f"Loaded dataset with {len(df)} rows")
        logger.info(f"Columns: {list(df.columns)}")
        
        return df
    
    def prepare_features(self, df):
        """Prepare features and target"""
        # Check available features
        available_features = []
        for col in self.required_features:
            if col in df.columns:
                available_features.append(col)
                df[col] = df[col].fillna(0)
            else:
                logger.warning(f"Column '{col}' not found in dataset")
        
        if not available_features:
            raise ValueError("No required feature columns found")
        
        # Check target column
        if 'experience_level' not in df.columns:
            raise ValueError("'experience_level' column not found in dataset")
        
        # Encode target labels
        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(df['experience_level'])
        
        # Prepare features
        X = df[available_features]
        
        logger.info(f"Training features: {available_features}")
        logger.info(f"Target classes: {list(label_encoder.classes_)}")
        logger.info(f"Class distribution: {dict(zip(*pd.Series(y).value_counts().items()))}")
        
        return X, y, label_encoder, available_features
    
    def train_model(self, X, y):
        """Train RandomForest classifier"""
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        logger.info(f"Training set: {len(X_train)} samples")
        logger.info(f"Test set: {len(X_test)} samples")
        
        # Train model
        model = RandomForestClassifier(
            n_estimators=100,
            class_weight='balanced',
            random_state=42,
            max_depth=10,
            min_samples_split=2
        )
        
        model.fit(X_train, y_train)
        
        # Evaluate
        train_score = accuracy_score(y_train, model.predict(X_train))
        test_score = accuracy_score(y_test, model.predict(X_test))
        
        logger.info(f"Training accuracy: {train_score:.4f}")
        logger.info(f"Test accuracy: {test_score:.4f}")
        
        # Detailed classification report
        y_pred = model.predict(X_test)
        logger.info("\nClassification Report:")
        logger.info(f"\n{classification_report(y_test, y_pred)}")
        
        return model
    
    def save_model(self, model, label_encoder, available_features):
        """Save trained model and metadata"""
        # Create models directory
        os.makedirs(self.model_dir, exist_ok=True)
        
        # Save model
        joblib.dump(model, self.model_path)
        logger.info(f"Model saved to {self.model_path}")
        
        # Save encoder
        joblib.dump(label_encoder, self.encoder_path)
        logger.info(f"Encoder saved to {self.encoder_path}")
        
        # Save feature list
        joblib.dump(available_features, self.features_path)
        logger.info(f"Features saved to {self.features_path}")
    
    def train(self):
        """Complete training pipeline"""
        try:
            logger.info("=" * 60)
            logger.info("EXPERIENCE LEVEL CLASSIFIER TRAINING")
            logger.info("=" * 60)
            
            # Load data
            df = self.load_data()
            
            # Prepare features
            X, y, label_encoder, available_features = self.prepare_features(df)
            
            # Train model
            model = self.train_model(X, y)
            
            # Save model
            self.save_model(model, label_encoder, available_features)
            
            logger.info("=" * 60)
            logger.info("TRAINING COMPLETED SUCCESSFULLY")
            logger.info("=" * 60)
            
            return True
            
        except Exception as e:
            logger.error(f"Training failed: {str(e)}")
            return False


def train_experience_model():
    """Convenience function to train experience model"""
    trainer = ExperienceClassifierTrainer()
    return trainer.train()


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Train model
    success = train_experience_model()
    
    if success:
        print("\n✅ Experience Level Model trained successfully!")
    else:
        print("\n❌ Experience Level Model training failed!")
