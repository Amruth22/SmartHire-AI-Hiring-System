# Helper Guide: Cleanup Unused Files

## Overview
This guide helps you identify and remove unused files from the SmartHire AI Hiring System. The system uses **ONLY GenAI (Gemini AI)** - no ML models are used.

---

## Files Safe to Remove

### 1. ML Analyzer (Not Used)
**File:** `analyzers/ml_analyzer.py`

**Reason:** All agents use AIAnalyzer (GenAI) only. MLAnalyzer is isolated and never called.

**Command:**
```bash
rm analyzers/ml_analyzer.py
```

**Impact:** None - no agent or workflow uses this file.

---

### 2. ML Model Files (If They Exist)
**Directory:** `models/`

**Files to check:**
- `models/experience_predictor_model.pkl`
- `models/resume_scorer_model.pkl`
- Any other `.pkl`, `.joblib`, or `.h5` files

**Reason:** System uses GenAI for all predictions, not pre-trained ML models.

**Commands:**
```bash
# Remove entire models directory if it exists
rm -rf models/

# Or remove specific model files
rm models/experience_predictor_model.pkl
rm models/resume_scorer_model.pkl
```

**Impact:** None - AIAnalyzer handles all predictions using Gemini.

---

### 3. Training Scripts (If They Exist)
**Files to check:**
- `train_models.py`
- `train_experience_model.py`
- `train_resume_scorer.py`
- Any file with "train" in the name

**Reason:** No ML models to train since system uses GenAI.

**Command:**
```bash
rm train_models.py
# Or any other training scripts
```

**Impact:** None - no training needed for GenAI system.

---

### 4. ML-Related Dependencies (Optional Cleanup)

**File:** `requirements.txt`

**Dependencies that can be removed:**
```txt
# These are NOT needed for GenAI-only system:
scikit-learn>=1.3.0
joblib>=1.3.0
numpy>=1.24.0  # Only if not used by other components
```

**Keep these (required):**
```txt
google-generativeai>=0.3.0  # GenAI - REQUIRED
streamlit>=1.28.0
sentence-transformers>=2.2.0  # For semantic analyzer
pandas>=2.0.0
PyPDF2>=3.0.0
python-dotenv>=1.0.0
```

**How to update:**
1. Edit `requirements.txt`
2. Remove ML-related packages
3. Reinstall dependencies:
```bash
pip install -r requirements.txt
```

---

## Verification After Cleanup

### 1. Check No Import Errors
```bash
python -c "from agents import *; from analyzers import AIAnalyzer, SemanticAnalyzer; print('All imports successful')"
```

### 2. Verify Agents Work
```bash
python -c "
from agents.experience_predictor_agent import ExperiencePredictorAgent
from agents.resume_scorer_agent import ResumeScorerAgent
agent1 = ExperiencePredictorAgent()
agent2 = ResumeScorerAgent()
print('Agents initialized successfully')
"
```

### 3. Check Workflow
```bash
python -c "
from workflows import build_hiring_workflow
workflow = build_hiring_workflow()
print('Workflow built successfully')
"
```

---

## Complete Cleanup Script

Create a file `cleanup.sh`:

```bash
#!/bin/bash

echo "Starting cleanup of unused ML files..."

# Remove ML analyzer
if [ -f "analyzers/ml_analyzer.py" ]; then
    echo "Removing analyzers/ml_analyzer.py..."
    rm analyzers/ml_analyzer.py
fi

# Remove models directory
if [ -d "models" ]; then
    echo "Removing models/ directory..."
    rm -rf models/
fi

# Remove training scripts
for file in train*.py; do
    if [ -f "$file" ]; then
        echo "Removing $file..."
        rm "$file"
    fi
done

# Remove __pycache__ for ml_analyzer
if [ -d "analyzers/__pycache__" ]; then
    echo "Cleaning analyzers/__pycache__..."
    rm -f analyzers/__pycache__/ml_analyzer.*
fi

echo "Cleanup complete!"
echo ""
echo "Verification:"
python3 -c "from agents import *; from analyzers import AIAnalyzer, SemanticAnalyzer; print('✓ All imports successful')"
```

**Make it executable and run:**
```bash
chmod +x cleanup.sh
./cleanup.sh
```

---

## Files to KEEP (Required)

### Core Architecture
- ✅ `config.py` - Configuration manager
- ✅ `state.py` - CandidateState dataclass
- ✅ `graph.py` - HiringGraph orchestrator
- ✅ `main.py` - Streamlit application

### Agents (All use GenAI)
- ✅ `agents/base_agent.py`
- ✅ `agents/resume_parser_agent.py`
- ✅ `agents/experience_predictor_agent.py`
- ✅ `agents/resume_scorer_agent.py`
- ✅ `agents/job_fit_analyzer_agent.py`
- ✅ `agents/question_generator_agent.py`
- ✅ `agents/answer_evaluator_agent.py`

### Analyzers (Tools)
- ✅ `analyzers/ai_analyzer.py` - GenAI tool (REQUIRED)
- ✅ `analyzers/semantic_analyzer.py` - SBERT tool (REQUIRED)
- ❌ `analyzers/ml_analyzer.py` - NOT USED (can remove)

### Nodes (Wrappers)
- ✅ All files in `nodes/` directory

### Workflows
- ✅ `workflows/hiring_workflow.py`

### Utils
- ✅ `utils/gemini_client.py`
- ✅ `utils/logging_utils.py`
- ✅ `utils/pdf_extractor.py`

### UI
- ✅ All files in `ui/` directory (if exists)

### Configuration
- ✅ `.env.example`
- ✅ `.gitignore`
- ✅ `requirements.txt`

---

## Post-Cleanup Checklist

- [ ] Removed `analyzers/ml_analyzer.py`
- [ ] Removed `models/` directory (if exists)
- [ ] Removed training scripts (if exist)
- [ ] Updated `requirements.txt` (optional)
- [ ] Verified no import errors
- [ ] Tested agent initialization
- [ ] Tested workflow building
- [ ] Ran Streamlit app successfully

---

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'analyzers.ml_analyzer'"

**Cause:** Some file still imports MLAnalyzer

**Solution:**
```bash
# Find files that import ml_analyzer
grep -r "from analyzers.ml_analyzer" .
grep -r "import ml_analyzer" .

# Should return no results after cleanup
```

### Error: "FileNotFoundError: models/experience_predictor_model.pkl"

**Cause:** MLAnalyzer tries to load model files

**Solution:** This shouldn't happen since MLAnalyzer is removed. If it does:
1. Check no agent imports MLAnalyzer
2. Verify `analyzers/__init__.py` doesn't export MLAnalyzer

---

## Summary

**What to Remove:**
- `analyzers/ml_analyzer.py` - Not used by any agent
- `models/` directory - No ML models needed
- Training scripts - No training needed for GenAI

**What to Keep:**
- Everything else - All required for GenAI-powered system

**System Uses:**
- ✅ Gemini AI (GenAI) for all predictions
- ✅ SBERT for semantic similarity
- ❌ NO ML models

---

## Questions?

If you're unsure about removing a file:

1. **Check imports:** `grep -r "filename" .`
2. **Check usage:** Search for the file name in all Python files
3. **Test without it:** Rename file to `.bak` and test system

**Safe rule:** If it's ML-related and not in the "KEEP" list above, it can be removed.
