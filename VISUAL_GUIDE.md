# SmartHire Visual Architecture Guide

This document provides visual representations of the SmartHire architecture.

---

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        SMARTHIRE SYSTEM                         │
│                  AI-Powered Hiring Platform                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      STREAMLIT UI (main.py)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Resume     │  │  Interview   │  │   Results    │         │
│  │   Analysis   │  │     Q&A      │  │  Evaluation  │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    WORKFLOW LAYER (workflows/)                  │
│                                                                 │
│  build_hiring_workflow()     build_evaluation_workflow()       │
│         │                              │                        │
│         └──────────────┬───────────────┘                        │
└────────────────────────┼────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                 ORCHESTRATION LAYER (graph.py)                  │
│                                                                 │
│                      HiringGraph Class                          │
│  ┌───────────────────────────────────────────────────────┐    │
│  │  run(state) → Execute Stages → Merge Results          │    │
│  └───────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   NODE LAYER (nodes/)                           │
│                                                                 │
│  resume_parser_node    experience_predictor_node               │
│  resume_scorer_node    job_fit_analyzer_node                   │
│  question_generator_node    answer_evaluator_node              │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   AGENT LAYER (agents/)                         │
│                                                                 │
│  ResumeParserAgent    ExperiencePredictorAgent                 │
│  ResumeScorerAgent    JobFitAnalyzerAgent                      │
│  QuestionGeneratorAgent    AnswerEvaluatorAgent                │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                 ANALYZER LAYER (analyzers/)                     │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ AIAnalyzer   │  │ MLAnalyzer   │  │  Semantic    │        │
│  │  (Gemini)    │  │ (sklearn)    │  │  Analyzer    │        │
│  │              │  │              │  │  (SBERT)     │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

```
┌─────────────┐
│   User      │
│   Input     │
└──────┬──────┘
       │
       │ Resume PDF + Job Description
       ▼
┌─────────────────────────────────────────┐
│      CandidateState (Initial)           │
│  - resume_text                          │
│  - job_description                      │
│  - job_title                            │
└──────┬──────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│   Stage 1: Resume Parsing               │
│   resume_parser_node                    │
│      ↓                                  │
│   ResumeParserAgent                     │
│      ↓                                  │
│   AIAnalyzer.parse_resume()             │
│      ↓                                  │
│   Gemini API Call (5-8s)                │
└──────┬──────────────────────────────────┘
       │
       │ + resume_features
       ▼
┌─────────────────────────────────────────┐
│   Stage 2: Experience Prediction        │
│   experience_predictor_node             │
│      ↓                                  │
│   ExperiencePredictorAgent              │
│      ↓                                  │
│   MLAnalyzer.predict_experience()       │
│      ↓                                  │
│   ML Model Inference (<1s)              │
└──────┬──────────────────────────────────┘
       │
       │ + experience_level
       ▼
┌─────────────────────────────────────────┐
│   Stage 3: Resume Scoring               │
│   resume_scorer_node                    │
│      ↓                                  │
│   ResumeScorerAgent                     │
│      ↓                                  │
│   MLAnalyzer.score_resume()             │
│      ↓                                  │
│   ML Model Inference (<1s)              │
└──────┬──────────────────────────────────┘
       │
       │ + resume_score
       ▼
┌─────────────────────────────────────────┐
│   Stage 4: Job Fit Analysis             │
│   job_fit_analyzer_node                 │
│      ↓                                  │
│   JobFitAnalyzerAgent                   │
│      ↓                                  │
│   AIAnalyzer.analyze_job_fit()          │
│      ↓                                  │
│   Gemini API Call (6-10s)               │
└──────┬──────────────────────────────────┘
       │
       │ + job_fit
       ▼
┌─────────────────────────────────────────┐
│   Stage 5: Question Generation          │
│   question_generator_node               │
│      ↓                                  │
│   QuestionGeneratorAgent                │
│      ↓                                  │
│   AIAnalyzer.generate_questions()       │
│      ↓                                  │
│   Gemini API Call (8-12s)               │
└──────┬──────────────────────────────────┘
       │
       │ + questions
       ▼
┌─────────────────────────────────────────┐
│      CandidateState (with questions)    │
│  - All previous data                    │
│  - questions: List[Dict]                │
└──────┬──────────────────────────────────┘
       │
       │ [USER ANSWERS QUESTIONS]
       │
       │ + answers
       ▼
┌─────────────────────────────────────────┐
│   Stage 6: Answer Evaluation            │
│   answer_evaluator_node                 │
│      ↓                                  │
│   AnswerEvaluatorAgent                  │
│      ↓                                  │
│   For each answer:                      │
│     if concept → SemanticAnalyzer       │
│     if code → AIAnalyzer                │
│      ↓                                  │
│   SBERT + Gemini (10-15s)               │
└──────┬──────────────────────────────────┘
       │
       │ + final_score, evaluated_answers
       ▼
┌─────────────────────────────────────────┐
│      CandidateState (Final)             │
│  - All analysis results                 │
│  - Evaluated answers                    │
│  - Final score                          │
│  - workflow_complete: True              │
└──────┬──────────────────────────────────┘
       │
       ▼
┌─────────────┐
│   Results   │
│   Display   │
└─────────────┘
```

---

## Layer Interaction Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                         USER REQUEST                           │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│  LAYER 5: ORCHESTRATION (graph.py)                            │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  HiringGraph.run(state)                                  │ │
│  │    - Execute stages sequentially                         │ │
│  │    - Handle errors                                       │ │
│  │    - Merge state                                         │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│  LAYER 4: WORKFLOWS (workflows/)                              │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  build_hiring_workflow()                                 │ │
│  │    - Define stage sequence                               │ │
│  │    - Configure parallelism                               │ │
│  │    - Return HiringGraph                                  │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│  LAYER 3: NODES (nodes/)                                      │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  resume_parser_node(state)                               │ │
│  │    - Call agent.analyze()                                │ │
│  │    - Update state                                        │ │
│  │    - Return state                                        │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│  LAYER 2: AGENTS (agents/)                                    │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  ResumeParserAgent.analyze(resume_text)                  │ │
│  │    - Use analyzer as tool                                │ │
│  │    - Coordinate analysis                                 │ │
│  │    - Return results                                      │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│  LAYER 1: ANALYZERS (analyzers/)                             │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  AIAnalyzer.parse_resume(text)                           │ │
│  │    - Call Gemini API                                     │ │
│  │    - Process response                                    │ │
│  │    - Return data                                         │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  Gemini API  │  │  ML Models   │  │    SBERT     │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└────────────────────────────────────────────────────────────────┘
```

---

## Agent-Analyzer Relationship

```
┌─────────────────────────────────────────────────────────────┐
│                         AGENTS                              │
│                      (Coordinators)                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ Uses as tools
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       ANALYZERS                             │
│                        (Tools)                              │
└─────────────────────────────────────────────────────────────┘

Specific Relationships:

ResumeParserAgent ──────────────► AIAnalyzer
                                  - parse_resume()

ExperiencePredictorAgent ───────► MLAnalyzer
                                  - predict_experience_level()

ResumeScorerAgent ──────────────► MLAnalyzer
                                  - score_resume()

JobFitAnalyzerAgent ────────────► AIAnalyzer
                                  - analyze_job_fit()

QuestionGeneratorAgent ─────────► AIAnalyzer
                                  - generate_questions()

AnswerEvaluatorAgent ───────────► SemanticAnalyzer
                        │         - evaluate_concept_answer()
                        │
                        └────────► AIAnalyzer
                                  - evaluate_code_answer()
```

---

## State Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│                    STATE CREATION                           │
│  CandidateState(                                            │
│    resume_text="...",                                       │
│    job_description="...",                                   │
│    job_title="..."                                          │
│  )                                                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                 STAGE 1: PARSING                            │
│  state.resume_features = {...}                             │
│  state.candidate_name = "John Doe"                         │
│  state.current_step = "resume_parsed"                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              STAGE 2: EXPERIENCE                            │
│  state.experience_level = "Mid-Level"                      │
│  state.experience_prediction_results = {...}               │
│  state.current_step = "experience_predicted"               │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                STAGE 3: SCORING                             │
│  state.resume_score = 7.5                                  │
│  state.resume_scoring_results = {...}                      │
│  state.current_step = "resume_scored"                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│               STAGE 4: JOB FIT                              │
│  state.job_fit = {...}                                     │
│  state.job_fit_results = {...}                             │
│  state.current_step = "job_fit_analyzed"                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              STAGE 5: QUESTIONS                             │
│  state.questions = [...]                                   │
│  state.current_step = "questions_generated"                │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ [USER INTERACTION]
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              STAGE 6: EVALUATION                            │
│  state.answers = [...]                                     │
│  state.final_score = 7.8                                   │
│  state.evaluation_results = {...}                          │
│  state.current_step = "completed"                          │
│  state.workflow_complete = True                            │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  FINAL STATE                                │
│  All fields populated                                       │
│  Ready for display/export                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Error Handling Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    OPERATION ATTEMPT                        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
                  ┌─────────┐
                  │ Success?│
                  └────┬────┘
                       │
           ┌───────────┴───────────┐
           │                       │
          YES                     NO
           │                       │
           ▼                       ▼
┌──────────────────┐    ┌──────────────────┐
│  Return Result   │    │  Catch Exception │
└──────────────────┘    └────────┬─────────┘
                                 │
                                 ▼
                        ┌──────────────────┐
                        │  Log Error       │
                        └────────┬─────────┘
                                 │
                                 ▼
                        ┌──────────────────┐
                        │  Try Fallback?   │
                        └────────┬─────────┘
                                 │
                     ┌───────────┴───────────┐
                     │                       │
                   YES                      NO
                     │                       │
                     ▼                       ▼
          ┌──────────────────┐    ┌──────────────────┐
          │  Use Fallback    │    │  Add to Errors   │
          │  Method          │    │  Return Default  │
          └────────┬─────────┘    └──────────────────┘
                   │
                   ▼
          ┌──────────────────┐
          │  Return Result   │
          └──────────────────┘

Example: AIAnalyzer.parse_resume()
  Try: Gemini API call
  Catch: Exception
  Fallback: Rule-based parsing
  Return: Features dict (always)
```

---

## Configuration Flow

```
┌─────────────────────────────────────────────────────────────┐
│                  APPLICATION START                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              ConfigManager.__init__()                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Load Default Config                            │
│  DEFAULT_CONFIG = {                                         │
│    "GEMINI_API_KEY_1": "",                                  │
│    "LOG_LEVEL": "INFO",                                     │
│    ...                                                      │
│  }                                                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│         Override with Environment Variables                 │
│  for key in config:                                         │
│    if os.environ.get(key):                                  │
│      config[key] = os.environ[key]                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Load from .env File                            │
│  if .env exists:                                            │
│    parse and override config                                │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Validate Configuration                         │
│  validate_config()                                          │
│    - Check required keys                                    │
│    - Raise error if missing                                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Configuration Ready                            │
│  get_config_value("GEMINI_API_KEY_1")                       │
└─────────────────────────────────────────────────────────────┘

Priority Order:
1. Environment Variables (highest)
2. .env File
3. Default Values (lowest)
```

---

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      DEPLOYMENT                             │
└─────────────────────────────────────────────────────────────┘

Option 1: Local Development
┌──────────────────────────────────────┐
│  Developer Machine                   │
│  ┌────────────────────────────────┐  │
│  │  streamlit run main.py         │  │
│  │  http://localhost:8501         │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘

Option 2: Docker Container
┌──────────────────────────────────────┐
│  Docker Container                    │
│  ┌────────────────────────────────┐  │
│  │  SmartHire Application         │  │
│  │  Port: 8501                    │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘

Option 3: Cloud Deployment
┌──────────────────────────────────────┐
│  Cloud Platform (AWS/GCP/Azure)      │
│  ┌────────────────────────────────┐  │
│  │  Load Balancer                 │  │
│  └──────────┬─────────────────────┘  │
│             │                         │
│    ┌────────┴────────┐                │
│    │                 │                │
│  ┌─▼──┐  ┌─▼──┐  ┌─▼──┐             │
│  │App1│  │App2│  │App3│             │
│  └────┘  └────┘  └────┘             │
│                                      │
│  ┌────────────────────────────────┐  │
│  │  Shared Storage (S3/GCS)       │  │
│  │  - Models                      │  │
│  │  - Logs                        │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘
```

---

## Performance Timeline

```
Time (seconds)
0s ────────────────────────────────────────────────────────► 45s

│
│ Resume Parsing (Gemini AI)
├─────────────────────────────────────────────────────────────►
│                                                    5-8s
│
│ Experience Prediction (ML)
├──►
│ <1s
│
│ Resume Scoring (ML)
├──►
│ <1s
│
│ Job Fit Analysis (Gemini AI)
├─────────────────────────────────────────────────────────────►
│                                                    6-10s
│
│ Question Generation (Gemini AI)
├─────────────────────────────────────────────────────────────►
│                                                    8-12s
│
│ [USER ANSWERS QUESTIONS]
│
│ Answer Evaluation (SBERT + Gemini)
├─────────────────────────────────────────────────────────────►
│                                                   10-15s
│
▼
Total: 30-45 seconds
```

---

This visual guide provides a comprehensive overview of the SmartHire architecture, data flow, and system interactions.

For more details, see:
- `ARCHITECTURE.md` - Detailed architecture documentation
- `README.md` - Main documentation
- `QUICKSTART.md` - Quick start guide
