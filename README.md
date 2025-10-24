# SmartHire - AI-Powered Intelligent Hiring System

**Multi-Agent Hiring System with Client Format Architecture**

A production-ready automated candidate evaluation system built following the client format pattern with proper separation of concerns.

---

## Overview

Automatically processes candidate resumes through a 5-stage analysis pipeline and generates personalized interview questions with intelligent answer evaluation in 30-45 seconds.

### Key Features

- **Client Format Architecture** - Agents, Analyzers, Workflows separation
- **Multi-Layer Design** - GenAI, ML, and Semantic analysis layers
- **Intelligent Orchestration** - Custom HiringGraph execution engine
- **@dataclass State** - With clone() and smart merge_from() methods
- **Dual Evaluation System** - SBERT for concepts, Gemini AI for code
- **ML-Powered Predictions** - Experience level and resume scoring
- **Personalized Questions** - Adapted to candidate profile

---

## Project Structure

```
SmartHire-AI-Hiring-System/
├── agents/                         # Agent CLASSES (coordinators)
│   ├── base_agent.py              # BaseAgent class
│   ├── resume_parser_agent.py     # Resume parsing coordinator
│   ├── experience_predictor_agent.py  # Experience prediction coordinator
│   ├── resume_scorer_agent.py     # Resume scoring coordinator
│   ├── job_fit_analyzer_agent.py  # Job fit coordinator
│   ├── question_generator_agent.py    # Question generation coordinator
│   └── answer_evaluator_agent.py  # Answer evaluation coordinator
│
├── analyzers/                      # Pure TOOLS (separate folder)
│   ├── ai_analyzer.py             # Gemini AI wrapper
│   ├── ml_analyzer.py             # ML models wrapper
│   └── semantic_analyzer.py       # SBERT wrapper
│
├── nodes/                          # Simplified business logic wrappers
│   ├── resume_parser_node.py      # Calls ResumeParserAgent
│   ├── experience_predictor_node.py   # Calls ExperiencePredictorAgent
│   ├── resume_scorer_node.py      # Calls ResumeScorerAgent
│   ├── job_fit_analyzer_node.py   # Calls JobFitAnalyzerAgent
│   ├── question_generator_node.py # Calls QuestionGeneratorAgent
│   └── answer_evaluator_node.py   # Calls AnswerEvaluatorAgent
│
├── workflows/                      # Workflow definitions
│   └── hiring_workflow.py         # build_hiring_workflow()
│
├── utils/                          # Utilities
│   ├── gemini_client.py           # Gemini API wrapper
│   ├── logging_utils.py           # Logging configuration
│   └── pdf_extractor.py           # PDF text extraction
│
├── data/                           # Training data and resumes
│   ├── resume/                    # PDF resume files
│   ├── job_descriptions.csv       # Job specifications
│   ├── experience_level_training_dataset.csv
│   └── resume_score_training_dataset.csv
│
├── models/                         # Trained ML models (auto-generated)
│   ├── experience_predictor_model.pkl
│   └── resume_scorer_model.pkl
│
├── graph.py                        # HiringGraph CLASS
├── state.py                        # CandidateState @dataclass
├── config.py                       # Configuration management
├── main.py                         # Streamlit application
├── train_models.py                 # ML model training script
├── requirements.txt                # Dependencies
└── .env.example                    # Configuration template
```

---

## Quick Start

### Installation

```bash
git clone https://github.com/Amruth22/SmartHire-AI-Hiring-System.git
cd SmartHire-AI-Hiring-System
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
mkdir logs models
```

### Configuration

```bash
cp .env.example .env
# Edit .env with your Gemini API keys
```

Required configuration:
```env
GEMINI_API_KEY_1=your_gemini_api_key_here
GEMINI_API_KEY_2=your_gemini_api_key_here
GEMINI_API_KEY_3=your_gemini_api_key_here
GEMINI_API_KEY_4=your_gemini_api_key_here
```

### Train ML Models (Important!)

```bash
python train_models.py
```

### Run Application

```bash
streamlit run main.py
```

---

## Architecture

### The Client Format Pattern

```
┌─────────────────────────────────────────┐
│         WORKFLOWS LAYER                 │
│      (workflow definitions)             │
│  • build_hiring_workflow()              │
│  • build_evaluation_workflow()          │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│         ORCHESTRATION LAYER             │
│            (graph.py)                   │
│  • HiringGraph class                    │
│  • Sequential execution engine          │
│  • Stage management                     │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│        BUSINESS LOGIC LAYER             │
│            (nodes/)                     │
│  • Thin wrappers                        │
│  • Call agents                          │
│  • Update state                         │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│           AGENT LAYER                   │
│           (agents/)                     │
│  • Agent classes                        │
│  • Coordinate analysis                  │
│  • Use analyzers as tools               │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│           TOOL LAYER                    │
│           (analyzers/)                  │
│  • Pure analysis tools                  │
│  • GenAI (Gemini)                       │
│  • ML (scikit-learn)                    │
│  • Semantic (SBERT)                     │
└─────────────────────────────────────────┘
```

---

## Workflow Execution

### 5-Stage Pipeline

```
Stage 1: Resume Parsing (AI-powered feature extraction)
    ↓
Stage 2: Experience Prediction (ML-based classification)
    ↓
Stage 3: Resume Scoring (ML-based quality assessment)
    ↓
Stage 4: Job Fit Analysis (AI-powered compatibility)
    ↓
Stage 5: Question Generation (AI-powered personalization)
    ↓
[USER ANSWERS QUESTIONS]
    ↓
Stage 6: Answer Evaluation (Semantic + AI evaluation)
```

**Performance**: 30-45 seconds for complete analysis

---

## Key Components

### Analyzers (Tools Layer)

**AIAnalyzer** - Gemini AI wrapper
- Resume parsing
- Job fit analysis
- Question generation
- Code answer evaluation

**MLAnalyzer** - ML models wrapper
- Experience level prediction
- Resume quality scoring
- Rule-based fallbacks

**SemanticAnalyzer** - SBERT wrapper
- Semantic similarity calculation
- Concept answer evaluation

### Agents (Coordinator Layer)

All agents inherit from `BaseAgent` and use analyzers as tools:
- **ResumeParserAgent** - Uses AIAnalyzer
- **ExperiencePredictorAgent** - Uses MLAnalyzer
- **ResumeScorerAgent** - Uses MLAnalyzer
- **JobFitAnalyzerAgent** - Uses AIAnalyzer
- **QuestionGeneratorAgent** - Uses AIAnalyzer
- **AnswerEvaluatorAgent** - Uses SemanticAnalyzer + AIAnalyzer

### Nodes (Wrapper Layer)

Simplified wrappers that:
1. Call agent's analyze() method
2. Update CandidateState
3. Return updated state

### Workflows (Builder Layer)

- `build_hiring_workflow()` - Main 5-stage pipeline
- `build_evaluation_workflow()` - Answer evaluation pipeline

---

## State Management

### CandidateState (@dataclass)

```python
@dataclass
class CandidateState:
    # Input data
    resume_text: str
    job_description: str
    job_title: str
    
    # Analysis results
    resume_features: Dict
    experience_level: str
    resume_score: float
    job_fit: Dict
    questions: List[Dict]
    answers: List[Dict]
    
    # Results
    final_score: float
    
    # Methods
    def clone() -> CandidateState
    def merge_from(other: CandidateState)
    def to_dict() -> Dict
```

---

## Separation of Concerns

### What Goes Where?

**Analyzers** (Pure Tools)
- ✅ AI/ML/Semantic operations
- ✅ Pure functions
- ❌ NO state management
- ❌ NO orchestration

**Agents** (Coordinators)
- ✅ Use analyzers as tools
- ✅ Coordinate analysis
- ❌ NO direct AI/ML calls
- ❌ NO state updates

**Nodes** (Wrappers)
- ✅ Call agents
- ✅ Update state
- ❌ NO business logic
- ❌ NO tool usage

**Workflows** (Builders)
- ✅ Define stage sequences
- ✅ Build graphs
- ❌ NO execution logic
- ❌ NO business logic

**Graph** (Orchestrator)
- ✅ Execute stages
- ✅ Manage state flow
- ❌ NO business logic
- ❌ NO tool usage

---

## Usage Example

```python
from state import CandidateState
from workflows import build_hiring_workflow
from utils import extract_text_from_pdf

# Extract resume text
resume_text = extract_text_from_pdf("resume.pdf")

# Create initial state
state = CandidateState(
    resume_text=resume_text,
    job_description="Software Engineer position...",
    job_title="Software Engineer"
)

# Build and run workflow
workflow = build_hiring_workflow()
result = workflow.run(state)

# Access results
print(f"Candidate: {result.candidate_name}")
print(f"Experience: {result.experience_level}")
print(f"Resume Score: {result.resume_score}/10")
print(f"Job Fit: {result.job_fit['job_fit']}")
print(f"Questions: {len(result.questions)}")
```

---

## ML Model Training

The system uses two ML models:

1. **Experience Predictor** (RandomForestClassifier)
   - Features: skills_count, projects_count, certifications_count, leadership, research
   - Output: Junior / Mid-Level / Senior

2. **Resume Scorer** (RandomForestRegressor)
   - Features: experience_years, skills_count, projects_count, certifications, education
   - Output: Score 0-10

Both models have rule-based fallbacks if training data is unavailable.

---

## Configuration Reference

### Required Variables

- `GEMINI_API_KEY_1` - Resume parsing
- `GEMINI_API_KEY_2` - Experience prediction & job fit
- `GEMINI_API_KEY_3` - Question generation
- `GEMINI_API_KEY_4` - Answer evaluation

### Optional Variables

- `GEMINI_MODEL` - Model name (default: gemini-2.0-flash)
- `CONFIDENCE_THRESHOLD` - Minimum confidence (default: 0.8)
- `MIN_RESUME_SCORE` - Minimum resume score (default: 5.0)
- `MIN_JOB_FIT_SCORE` - Minimum job fit score (default: 6.0)
- `LOG_LEVEL` - Logging level (default: INFO)
- `MAX_WORKERS` - Parallel workers (default: 3)

---

## Learning Value

This project demonstrates:
- ✅ Client format architecture pattern
- ✅ Proper separation of concerns
- ✅ Agent/Analyzer/Node separation
- ✅ Custom graph execution engine
- ✅ @dataclass state management with smart merge
- ✅ Workflow builder pattern
- ✅ Multi-layer AI/ML integration
- ✅ Production-ready code structure

---

## Status

**PRODUCTION READY**

- ✅ All agents implemented (6 agents)
- ✅ All analyzers implemented (3 tools)
- ✅ All nodes implemented (6 nodes)
- ✅ Workflow builders complete
- ✅ HiringGraph class complete
- ✅ State management complete
- ✅ Configuration management complete
- ✅ Utils complete (Gemini, logging, PDF)
- ✅ ML model training script complete

---

## License

MIT License

---

## Acknowledgments

- **Client Format Pattern** - Based on ai-incident-response-client-format reference
- **LangGraph Principles** - For multi-agent orchestration concepts

---

**Built with proper separation of concerns following client format architecture**

**Repository**: https://github.com/Amruth22/SmartHire-AI-Hiring-System

**Status**: PRODUCTION READY
