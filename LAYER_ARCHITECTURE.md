# SmartHire - 3-Layer Architecture Documentation

## Overview

SmartHire implements a **3-layer architecture** separating Agentic AI, GenAI, and ML concerns for maintainability, scalability, and clarity.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                        │
│                      (main.py)                              │
│              Streamlit UI + Orchestration                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   AGENTIC AI LAYER                          │
│              (agents/, nodes/, workflows/)                  │
│                                                             │
│  • Multi-agent orchestration                               │
│  • Workflow coordination                                   │
│  • Business logic                                          │
│  • State management                                        │
│                                                             │
│  Components:                                               │
│  - 6 Specialized Agents (coordinators)                    │
│  - 6 Node Wrappers (state updaters)                       │
│  - 2 Workflow Builders (pipeline definitions)             │
│  - HiringGraph (execution engine)                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
        ┌───────────────────┴───────────────────┐
        ↓                                       ↓
┌──────────────────────────┐    ┌──────────────────────────┐
│     GENAI LAYER          │    │      ML LAYER            │
│  (genai_layer/)          │    │   (ml_layer/)            │
│                          │    │                          │
│  • LLM Services          │    │  • Traditional ML        │
│  • Embeddings            │    │  • Scikit-learn          │
│  • NLP Analysis          │    │  • Classification        │
│  • Generation            │    │  • Regression            │
│                          │    │                          │
│  Tools:                  │    │  Tools:                  │
│  - Gemini 2.0 Flash      │    │  - RandomForest          │
│  - SBERT Embeddings      │    │  - Experience Classifier │
│  - Resume Parser         │    │  - Resume Scorer         │
│  - Job Fit Analyzer      │    │                          │
│  - Question Generator    │    │                          │
│  - Answer Evaluator      │    │                          │
└──────────────────────────┘    └──────────────────────────┘
```

---

## Layer 1: Agentic AI Layer

### Location
```
agents/                    # Agent coordinators
nodes/                     # Node wrappers
workflows/                 # Workflow builders
graph.py                   # Execution engine
state.py                   # State management
```

### Purpose
Orchestrates the entire hiring workflow using multi-agent collaboration.

### Components

#### **Agents (Coordinators)**
1. `ResumeParserAgent` - Coordinates resume parsing
2. `ExperiencePredictorAgent` - Coordinates experience prediction
3. `ResumeScorerAgent` - Coordinates resume scoring
4. `JobFitAnalyzerAgent` - Coordinates job fit analysis
5. `QuestionGeneratorAgent` - Coordinates question generation
6. `AnswerEvaluatorAgent` - Coordinates answer evaluation

**Key Characteristic**: Agents coordinate but don't perform analysis directly. They use GenAI and ML layers as tools.

#### **Nodes (Wrappers)**
Thin wrappers that:
1. Call agent's `analyze()` method
2. Update `CandidateState`
3. Return updated state

#### **Workflows (Builders)**
Define stage sequences:
- `build_hiring_workflow()` - 5-stage analysis pipeline
- `build_evaluation_workflow()` - Answer evaluation pipeline

#### **Graph (Orchestrator)**
`HiringGraph` class:
- Executes stages sequentially
- Supports parallel node execution
- Manages state flow
- Handles errors

### Responsibilities
- ✅ Multi-agent coordination
- ✅ Workflow orchestration
- ✅ Business logic
- ✅ State management
- ❌ NO direct AI/ML operations
- ❌ NO tool implementation

---

## Layer 2: GenAI Layer

### Location
```
genai_layer/
├── llm/                   # LLM services
│   ├── gemini_service.py
│   └── prompt_templates.py
├── embeddings/            # Embedding services
│   ├── sbert_service.py
│   └── embedding_cache.py
├── analysis/              # Analysis tools
│   ├── resume_parser.py
│   ├── job_fit_analyzer.py
│   ├── question_generator.py
│   └── answer_evaluator.py
└── README.md
```

### Purpose
Provides Generative AI capabilities using Gemini 2.0 Flash and SBERT.

### Components

#### **LLM Services**
- `GeminiService` - Wrapper for Gemini API with retry logic
- Prompt templates for structured output
- JSON response cleaning and validation

#### **Embeddings**
- SBERT (Sentence-BERT) for semantic similarity
- Embedding caching for performance
- Used for concept question evaluation

#### **Analysis Tools**
1. **Resume Parser** - Extracts structured data from resume text
2. **Job Fit Analyzer** - Analyzes candidate-job compatibility
3. **Question Generator** - Creates personalized interview questions
4. **Answer Evaluator** - Evaluates answers with AI

### Responsibilities
- ✅ Natural language understanding
- ✅ Text generation
- ✅ Semantic analysis
- ✅ Embedding generation
- ❌ NO orchestration logic
- ❌ NO state management

### API Configuration
- `GEMINI_API_KEY_1` - Resume parsing
- `GEMINI_API_KEY_2` - Job fit analysis
- `GEMINI_API_KEY_3` - Question generation
- `GEMINI_API_KEY_4` - Answer evaluation

---

## Layer 3: ML Layer

### Location
```
ml_layer/
├── training/              # Model training
│   ├── experience_classifier_trainer.py
│   ├── resume_scorer_trainer.py
│   └── train_all_models.py
├── inference/             # Prediction logic
│   ├── experience_predictor.py
│   └── resume_scorer.py
├── models/                # Trained models (created after training)
│   ├── experience_level_model.pkl
│   ├── experience_level_encoder.pkl
│   ├── resume_score_model.pkl
│   └── resume_score_scaler.pkl
└── README.md
```

### Purpose
Provides traditional ML models for fast, deterministic predictions.

### Components

#### **Training Module**
1. **ExperienceClassifierTrainer**
   - Trains RandomForestClassifier
   - Features: experience_years, skills_count, project_count, leadership
   - Output: Junior / Mid-Level / Senior

2. **ResumeScorerTrainer**
   - Trains RandomForestRegressor
   - Features: experience, skills, projects, certifications, leadership, research
   - Output: Score 0-10

3. **train_all_models.py**
   - Main script to train all models
   - Creates models directory
   - Saves trained models as .pkl files

#### **Inference Module**
1. **ExperiencePredictor**
   - Loads trained classifier
   - Predicts experience level
   - Fallback to rule-based if model unavailable

2. **ResumeScorer**
   - Loads trained regressor
   - Predicts resume score
   - Fallback to rule-based if model unavailable

### Responsibilities
- ✅ Traditional ML predictions
- ✅ Fast classification/regression
- ✅ Deterministic scoring
- ✅ Model training and persistence
- ❌ NO orchestration logic
- ❌ NO state management

### Training Data
- `data/experience_level_training_dataset.csv` - 32 samples
- `data/resume_score_training_dataset.csv` - 32 samples

---

## Data Flow

### Complete Pipeline

```
1. User uploads resume + selects job
        ↓
2. Agentic Layer creates initial CandidateState
        ↓
3. Stage 1: Resume Parsing
   - Agent: ResumeParserAgent
   - Tool: GenAI Layer (resume_parser)
   - Updates: state.resume_features
        ↓
4. Stage 2: Experience Prediction
   - Agent: ExperiencePredictorAgent
   - Tool: ML Layer (experience_predictor)
   - Updates: state.experience_level
        ↓
5. Stage 3: Resume Scoring
   - Agent: ResumeScorerAgent
   - Tool: ML Layer (resume_scorer)
   - Updates: state.resume_score
        ↓
6. Stage 4: Job Fit Analysis
   - Agent: JobFitAnalyzerAgent
   - Tool: GenAI Layer (job_fit_analyzer)
   - Updates: state.job_fit
        ↓
7. Stage 5: Question Generation
   - Agent: QuestionGeneratorAgent
   - Tool: GenAI Layer (question_generator)
   - Updates: state.questions
        ↓
8. User answers questions
        ↓
9. Stage 6: Answer Evaluation
   - Agent: AnswerEvaluatorAgent
   - Tools: GenAI Layer (answer_evaluator) + SBERT
   - Updates: state.answers, state.final_score
        ↓
10. Display final results
```

---

## Layer Interaction Rules

### What Each Layer Can Do

| Layer | Can Use | Cannot Use |
|-------|---------|------------|
| **Agentic** | GenAI Layer, ML Layer, State | Direct AI/ML calls |
| **GenAI** | Gemini API, SBERT | Agents, State, ML models |
| **ML** | Scikit-learn, Joblib | Agents, State, GenAI |

### Communication Pattern

```
Agentic Layer (Orchestrator)
    ↓ calls
GenAI Layer (Tool) → returns result
    ↑ uses
Gemini API / SBERT

Agentic Layer (Orchestrator)
    ↓ calls
ML Layer (Tool) → returns result
    ↑ uses
Scikit-learn Models
```

---

## Separation of Concerns

### Agentic Layer
- **Responsibility**: Orchestration and coordination
- **Does**: Manages workflow, coordinates agents, updates state
- **Doesn't**: Perform AI/ML operations directly

### GenAI Layer
- **Responsibility**: Generative AI operations
- **Does**: NLP, text generation, semantic analysis
- **Doesn't**: Orchestrate workflows, manage state

### ML Layer
- **Responsibility**: Traditional ML predictions
- **Does**: Classification, regression, model training
- **Doesn't**: Orchestrate workflows, manage state

---

## Benefits of This Architecture

### 1. Clear Separation
Each layer has a single, well-defined responsibility.

### 2. Easy Testing
- Test agents independently
- Test GenAI tools independently
- Test ML models independently

### 3. Scalability
- Scale GenAI layer (more API keys, caching)
- Scale ML layer (GPU, batch processing)
- Scale Agentic layer (parallel execution)

### 4. Maintainability
- Change GenAI provider without touching agents
- Update ML models without changing workflow
- Add new agents without modifying tools

### 5. Flexibility
- Use GenAI for some tasks, ML for others
- Fallback from GenAI to ML or vice versa
- Mix and match based on requirements

---

## Training ML Models

### Before First Use

```bash
# Train all ML models
python ml_layer/training/train_all_models.py

# Or train individually
python ml_layer/training/experience_classifier_trainer.py
python ml_layer/training/resume_scorer_trainer.py
```

### Output
Models saved to `ml_layer/models/`:
- `experience_level_model.pkl`
- `experience_level_encoder.pkl`
- `experience_features.pkl`
- `resume_score_model.pkl`
- `resume_score_scaler.pkl`
- `resume_score_features.pkl`

---

## Using the Layers

### From Agents

```python
# Using GenAI Layer
from genai_layer.analysis import resume_parser
result = resume_parser.parse_resume(resume_text)

# Using ML Layer
from ml_layer.inference import experience_predictor
result = experience_predictor.predict(resume_features)
```

### From Application

```python
# Build workflow (uses all layers internally)
from workflows import build_hiring_workflow

workflow = build_hiring_workflow()
result = workflow.run(initial_state)
```

---

## Performance Characteristics

### GenAI Layer
- **Speed**: 5-12 seconds per operation
- **Accuracy**: High (depends on prompt quality)
- **Cost**: API calls (rate limited)
- **Use For**: Complex analysis, generation, NLP

### ML Layer
- **Speed**: <1 second per prediction
- **Accuracy**: Good (depends on training data)
- **Cost**: Free (after training)
- **Use For**: Fast classification, scoring

---

## Summary

SmartHire's 3-layer architecture provides:

1. **Agentic Layer** - Orchestrates the workflow
2. **GenAI Layer** - Provides AI-powered analysis
3. **ML Layer** - Provides fast ML predictions

Each layer is independent, testable, and scalable. Agents coordinate between layers without performing analysis directly, ensuring clean separation of concerns.

---

**Status**: ✅ All 3 layers fully implemented and documented
