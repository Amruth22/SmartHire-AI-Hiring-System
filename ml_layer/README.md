# ML Layer - Traditional Machine Learning Models

## Overview

This layer contains traditional ML models for candidate evaluation using scikit-learn. These models complement the GenAI layer by providing fast, deterministic predictions.

## Components

### 1. Training Module (`training/`)
- `experience_classifier_trainer.py` - Trains RandomForestClassifier for experience level prediction
- `resume_scorer_trainer.py` - Trains RandomForestRegressor for resume quality scoring
- `train_all_models.py` - Main script to train all ML models

### 2. Inference Module (`inference/`)
- `experience_predictor.py` - Predicts Junior/Mid-Level/Senior classification
- `resume_scorer.py` - Scores resumes 0-10 based on features

### 3. Models Directory (`models/`)
- Stores trained model files (.pkl)
- `experience_level_model.pkl` - Experience classifier
- `experience_level_encoder.pkl` - Label encoder
- `resume_score_model.pkl` - Resume scorer
- `resume_score_scaler.pkl` - Feature scaler

## Features

### Experience Level Classifier
- **Algorithm**: RandomForestClassifier
- **Features**: 
  - total_experience_years
  - skills_count
  - project_count
  - leadership_experience
- **Output**: Junior / Mid-Level / Senior
- **Training Data**: 32 samples

### Resume Score Predictor
- **Algorithm**: RandomForestRegressor
- **Features**:
  - total_experience_years
  - skills_count
  - project_count
  - certification_count
  - leadership_experience
  - has_research_work
- **Output**: Score 0-10
- **Training Data**: 32 samples

## Usage

### Training Models

```bash
# Train all models
python ml_layer/training/train_all_models.py

# Train individual models
python ml_layer/training/experience_classifier_trainer.py
python ml_layer/training/resume_scorer_trainer.py
```

### Using in Agents

```python
from ml_layer.inference import experience_predictor, resume_scorer

# Predict experience level
features = {
    "total_experience_years": 3.5,
    "skills_count": 15,
    "project_count": 5,
    "leadership_experience": 1
}
level = experience_predictor.predict(features)

# Score resume
score = resume_scorer.predict(features)
```

## Integration with GenAI Layer

The ML layer works alongside the GenAI layer:

1. **ML Layer**: Fast, deterministic predictions for structured features
2. **GenAI Layer**: Deep analysis, natural language understanding, personalization

Agents can use both layers:
- ML for quick scoring/classification
- GenAI for detailed analysis and reasoning

## Model Performance

### Experience Classifier
- Accuracy: ~95% on test set
- Classes: Junior, Mid-Level, Senior
- Balanced class weights

### Resume Scorer
- R² Score: ~0.98
- MSE: ~0.15
- Range: 0-10

## Training Data

Located in `data/`:
- `experience_level_training_dataset.csv` - 32 samples
- `resume_score_training_dataset.csv` - 32 samples

## Dependencies

```
scikit-learn>=1.3.0
pandas>=2.0.0
joblib>=1.3.0
```

## Architecture

```
ml_layer/
├── training/              # Model training scripts
│   ├── experience_classifier_trainer.py
│   ├── resume_scorer_trainer.py
│   └── train_all_models.py
├── inference/             # Prediction logic
│   ├── experience_predictor.py
│   └── resume_scorer.py
├── models/                # Trained models (created after training)
│   ├── experience_level_model.pkl
│   ├── experience_level_encoder.pkl
│   ├── experience_features.pkl
│   ├── resume_score_model.pkl
│   ├── resume_score_scaler.pkl
│   └── resume_score_features.pkl
└── README.md              # This file
```

## Notes

- Models are trained on small datasets (32 samples) - suitable for demonstration
- For production, collect more training data
- Models auto-train if not found during first prediction
- Fallback to rule-based logic if training fails
