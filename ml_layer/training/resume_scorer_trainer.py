"""
Resume Score Predictor Trainer

Trains a RandomForestRegressor to predict resume quality score (0-10)
based on candidate features.
"""

import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import logging

logger = logging.getLogger("ml_layer.training.resume_scorer")


class ResumeScorerTrainer:
    """Trains resume scoring regression model"""
    
    def __init__(self, dataset_path="data/resume_score_training_dataset.csv"):
        """
        Initialize trainer
        
        Args:
            dataset_path: Path to training dataset CSV
        """
        self.dataset_path = dataset_path
        self.model_dir = "ml_layer/models"
        self.model_path = os.path.join(self.model_dir, "resume_score_model.pkl")
        self.scaler_path = os.path.join(self.model_dir, "resume_score_scaler.pkl")
        self.features_path = os.path.join(self.model_dir, "resume_score_features.pkl")
        
        self.required_features = [
            'total_experience_years',
            'skills_count',
            'project_count',
            'certification_count',
            'leadership_experience',
            'has_research_work'
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
        if 'resume_score' not in df.columns:
            raise ValueError("'resume_score' column not found in dataset")
        
        # Prepare features and target
        X = df[available_features]
        y = df['resume_score']
        
        logger.info(f"Training features: {available_features}")
        logger.info(f"Score range: {y.min():.2f} - {y.max():.2f}")
        logger.info(f"Score mean: {y.mean():.2f}, std: {y.std():.2f}")
        
        return X, y, available_features
    
    def train_model(self, X, y):
        """Train RandomForest regressor"""
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        logger.info(f"Training set: {len(X_train)} samples")
        logger.info(f"Test set: {len(X_test)} samples")
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model
        model = RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            max_depth=10,
            min_samples_split=2,
            min_samples_leaf=1
        )
        
        model.fit(X_train_scaled, y_train)
        
        # Evaluate
        train_pred = model.predict(X_train_scaled)
        test_pred = model.predict(X_test_scaled)
        
        train_r2 = r2_score(y_train, train_pred)
        test_r2 = r2_score(y_test, test_pred)
        train_mse = mean_squared_error(y_train, train_pred)
        test_mse = mean_squared_error(y_test, test_pred)
        train_mae = mean_absolute_error(y_train, train_pred)
        test_mae = mean_absolute_error(y_test, test_pred)
        
        logger.info("\nModel Performance:")
        logger.info(f"Training R² Score: {train_r2:.4f}")
        logger.info(f"Test R² Score: {test_r2:.4f}")
        logger.info(f"Training MSE: {train_mse:.4f}")
        logger.info(f"Test MSE: {test_mse:.4f}")
        logger.info(f"Training MAE: {train_mae:.4f}")
        logger.info(f"Test MAE: {test_mae:.4f}")
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        logger.info("\nFeature Importance:")
        for _, row in feature_importance.iterrows():
            logger.info(f"  {row['feature']}: {row['importance']:.4f}")
        
        return model, scaler
    
    def save_model(self, model, scaler, available_features):
        """Save trained model and metadata"""
        # Create models directory
        os.makedirs(self.model_dir, exist_ok=True)
        
        # Save model
        joblib.dump(model, self.model_path)
        logger.info(f"Model saved to {self.model_path}")
        
        # Save scaler
        joblib.dump(scaler, self.scaler_path)
        logger.info(f"Scaler saved to {self.scaler_path}")
        
        # Save feature list
        joblib.dump(available_features, self.features_path)
        logger.info(f"Features saved to {self.features_path}")
    
    def train(self):
        """Complete training pipeline"""
        try:
            logger.info("=" * 60)
            logger.info("RESUME SCORE PREDICTOR TRAINING")
            logger.info("=" * 60)
            
            # Load data
            df = self.load_data()
            
            # Prepare features
            X, y, available_features = self.prepare_features(df)
            
            # Train model
            model, scaler = self.train_model(X, y)
            
            # Save model
            self.save_model(model, scaler, available_features)
            
            logger.info("=" * 60)
            logger.info("TRAINING COMPLETED SUCCESSFULLY")
            logger.info("=" * 60)
            
            return True
            
        except Exception as e:
            logger.error(f"Training failed: {str(e)}")
            return False


def train_resume_score_model():
    """Convenience function to train resume score model"""
    trainer = ResumeScorerTrainer()
    return trainer.train()


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Train model
    success = train_resume_score_model()
    
    if success:
        print("\n✅ Resume Score Model trained successfully!")
    else:
        print("\n❌ Resume Score Model training failed!")
