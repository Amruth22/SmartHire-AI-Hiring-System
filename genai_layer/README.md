# GenAI Layer - Generative AI Services

## Overview

This layer contains all Generative AI services using Google's Gemini 2.0 Flash model. It provides natural language understanding, generation, and analysis capabilities.

## Components

### 1. LLM Service (`llm/`)
- `gemini_service.py` - Gemini AI wrapper with retry logic and error handling
- `prompt_templates.py` - Reusable prompt templates

### 2. Embeddings (`embeddings/`)
- `sbert_service.py` - Sentence-BERT embeddings for semantic similarity
- `embedding_cache.py` - Caching layer for embeddings

### 3. Analysis Tools (`analysis/`)
- `resume_parser.py` - AI-powered resume parsing
- `job_fit_analyzer.py` - Job compatibility analysis
- `question_generator.py` - Personalized question generation
- `answer_evaluator.py` - Answer evaluation with AI

## Features

### Resume Parsing
- Extracts structured data from unstructured resume text
- Returns JSON with name, email, skills, experience, education, etc.
- Handles various resume formats

### Job Fit Analysis
- Analyzes compatibility between candidate and job
- Identifies matching skills and gaps
- Provides fit score (0-10) and reasoning

### Question Generation
- Creates personalized interview questions
- Adapts to candidate experience level
- Mixes concept and coding questions
- Includes reference answers

### Answer Evaluation
- Evaluates concept answers using semantic similarity (SBERT)
- Evaluates code answers using AI analysis
- Provides detailed feedback and scores

## API Configuration

Uses 4 Gemini API keys for load balancing:
- `GEMINI_API_KEY_1` - Resume parsing
- `GEMINI_API_KEY_2` - Job fit analysis
- `GEMINI_API_KEY_3` - Question generation
- `GEMINI_API_KEY_4` - Answer evaluation

## Usage

### Resume Parsing

```python
from genai_layer.analysis import resume_parser

result = resume_parser.parse_resume(resume_text)
# Returns: {full_name, email, skills, experience, ...}
```

### Job Fit Analysis

```python
from genai_layer.analysis import job_fit_analyzer

result = job_fit_analyzer.analyze_fit(
    resume_features=features,
    job_description=job_desc,
    job_title=title
)
# Returns: {job_fit, fit_score, reason, matching_skills, missing_skills}
```

### Question Generation

```python
from genai_layer.analysis import question_generator

questions = question_generator.generate_questions(
    experience_level="Mid-Level",
    job_title="Software Engineer",
    resume_features=features
)
# Returns: List of question dictionaries
```

### Answer Evaluation

```python
from genai_layer.analysis import answer_evaluator

result = answer_evaluator.evaluate_answer(
    question=question,
    reference_answer=ref_answer,
    student_answer=student_answer,
    question_type="concept"  # or "code"
)
# Returns: {score, feedback, method}
```

## Integration with ML Layer

The GenAI layer complements the ML layer:

1. **ML Layer**: Fast, structured predictions (experience level, resume score)
2. **GenAI Layer**: Deep analysis, natural language understanding, personalization

Agents use both layers:
- ML for quick classification/scoring
- GenAI for detailed analysis and reasoning

## Model Configuration

### Gemini 2.0 Flash
- Model: `gemini-2.0-flash`
- Temperature: 0.1 (deterministic)
- Top-p: 0.8
- Top-k: 40
- Max tokens: 1024-2048 (varies by task)

### SBERT
- Model: `all-MiniLM-L6-v2`
- Embedding dimension: 384
- Fast inference on CPU

## Error Handling

All services include:
- Retry logic with exponential backoff
- Fallback mechanisms
- Comprehensive error logging
- Graceful degradation

## Performance

- Resume parsing: 5-8 seconds
- Job fit analysis: 5-8 seconds
- Question generation: 8-12 seconds
- Answer evaluation: 5-10 seconds

## Architecture

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
└── README.md              # This file
```

## Dependencies

```
google-generativeai>=0.3.0
langchain>=0.3.7
langchain-google-genai>=2.0.5
sentence-transformers>=2.2.2
```

## Notes

- All GenAI operations use Gemini 2.0 Flash
- SBERT is used only for semantic similarity (concept questions)
- Prompt templates are optimized for structured output
- JSON responses are cleaned and validated
