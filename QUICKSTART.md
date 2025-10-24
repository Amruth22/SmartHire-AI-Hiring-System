# SmartHire Quick Start Guide

Get up and running with SmartHire in 5 minutes!

---

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://aistudio.google.com))
- Git

---

## Installation Steps

### 1. Clone Repository

```bash
git clone https://github.com/Amruth22/SmartHire-AI-Hiring-System.git
cd SmartHire-AI-Hiring-System
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your API keys
# You can use the same key for all 4 variables if you only have one
nano .env  # or use any text editor
```

Your `.env` should look like:
```env
GEMINI_API_KEY_1=your_actual_api_key_here
GEMINI_API_KEY_2=your_actual_api_key_here
GEMINI_API_KEY_3=your_actual_api_key_here
GEMINI_API_KEY_4=your_actual_api_key_here
```

### 5. Create Required Directories

```bash
mkdir -p logs models data/resume
```

### 6. Prepare Training Data (Optional)

If you have training datasets, place them in the `data/` directory:
- `data/experience_level_training_dataset.csv`
- `data/resume_score_training_dataset.csv`
- `data/job_descriptions.csv`

### 7. Train ML Models (Optional but Recommended)

```bash
python train_models.py
```

If you don't have training data, the system will use rule-based fallbacks.

### 8. Add Resume Files

Place PDF resumes in subdirectories under `data/resume/`:

```bash
mkdir -p data/resume/Software_Developer
mkdir -p data/resume/Data_Engineer
# Add your PDF files to these directories
```

### 9. Run the Application

```bash
streamlit run main.py
```

The application will open in your browser at `http://localhost:8501`

---

## First Time Usage

### Step 1: Upload Resume

1. Select a designation (e.g., Software Developer)
2. Select a resume PDF file
3. Select a job role

### Step 2: Run Analysis

Click "Start AI Analysis" button. The system will:
- Parse the resume (5-8 seconds)
- Predict experience level (<1 second)
- Score resume quality (<1 second)
- Analyze job fit (6-10 seconds)
- Generate interview questions (8-12 seconds)

Total time: ~30-45 seconds

### Step 3: Answer Questions

1. Go to "Interview Q&A Session" tab
2. Answer all generated questions
3. Click "Submit All Answers"

### Step 4: View Results

1. Go to "Results & Evaluation" tab
2. View detailed scores and feedback
3. Download report if needed

---

## Troubleshooting

### Issue: "Configuration Error: Missing required configuration"

**Solution**: Make sure your `.env` file has at least `GEMINI_API_KEY_1` set.

### Issue: "Failed to extract text from PDF"

**Solution**: 
- Ensure PDF is text-based (not scanned image)
- Try a different PDF file
- Check file permissions

### Issue: "ML model not found"

**Solution**: 
- Run `python train_models.py` to train models
- Or continue without models (system will use rule-based fallbacks)

### Issue: "Gemini API rate limit exceeded"

**Solution**:
- Wait a few minutes
- Use multiple API keys (one for each variable in .env)
- Reduce request frequency

### Issue: "Module not found"

**Solution**:
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

---

## Sample Data Format

### Job Descriptions CSV

```csv
job_title,job_summary,required_skills,preferred_skills,min_required_experience,max_required_experience,difficulty_level
Software Engineer,"Develop and maintain software applications","Python,Java,SQL","AWS,Docker",2,5,Medium
Data Engineer,"Build data pipelines","Python,SQL,Spark","Airflow,Kafka",3,7,High
```

### Experience Level Training CSV

```csv
skills_count,projects_count,certifications_count,leadership_experience,has_research_work,experience_level
5,2,0,0,0,Junior
10,4,2,1,0,Mid-Level
15,6,3,1,1,Senior
```

### Resume Score Training CSV

```csv
total_experience_years,skills_count,projects_count,certifications_count,education_level,resume_score
1.5,5,2,0,2,5.5
3.5,10,4,2,2,7.5
6.0,15,6,3,3,9.0
```

---

## Architecture Overview

```
User → Streamlit UI → Workflows → Graph → Nodes → Agents → Analyzers
                                                              ↓
                                                    GenAI / ML / SBERT
```

**5 Layers**:
1. **Analyzers** - Pure tools (AI, ML, Semantic)
2. **Agents** - Coordinators (use analyzers)
3. **Nodes** - Wrappers (call agents, update state)
4. **Workflows** - Builders (define stages)
5. **Graph** - Orchestrator (execute workflow)

---

## Next Steps

1. **Add More Resumes**: Place PDF files in `data/resume/` subdirectories
2. **Customize Job Descriptions**: Edit `data/job_descriptions.csv`
3. **Train Better Models**: Add more training data and retrain
4. **Explore Code**: Check `ARCHITECTURE.md` for detailed design
5. **Customize Workflows**: Modify `workflows/hiring_workflow.py`

---

## Getting Help

- **Documentation**: See `README.md` and `ARCHITECTURE.md`
- **Issues**: Create an issue on GitHub
- **Architecture**: Read `ARCHITECTURE.md` for design details

---

## Quick Commands Reference

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Train models
python train_models.py

# Run application
streamlit run main.py

# Install dependencies
pip install -r requirements.txt

# Check logs
tail -f logs/smarthire.log
```

---

**You're all set! Start evaluating candidates with AI-powered intelligence.**
