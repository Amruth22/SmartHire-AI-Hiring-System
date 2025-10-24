# Data Directory

This directory contains training datasets and resume files for the SmartHire system.

## Structure

```
data/
├── resume/                    # PDF resume files organized by category
│   ├── Data_Engineer/
│   ├── Software_Developer/
│   ├── Software_Engineer/
│   └── Test_Engineer/
├── job_descriptions.csv       # Job role specifications
├── experience_level_training_dataset.csv  # ML training data
└── resume_score_training_dataset.csv      # ML training data
```

## Required Files

### 1. job_descriptions.csv

Columns:
- job_title
- job_summary
- required_skills
- preferred_skills
- min_required_experience
- max_required_experience
- difficulty_level

### 2. experience_level_training_dataset.csv

Columns:
- skills_count
- projects_count
- certifications_count
- leadership_experience
- has_research_work
- experience_level (Junior/Mid-Level/Senior)

### 3. resume_score_training_dataset.csv

Columns:
- total_experience_years
- skills_count
- projects_count
- certifications_count
- education_level
- resume_score (0-10)

## Resume Files

Place PDF resume files in the `resume/` subdirectories organized by job category.

Example:
```
data/resume/Software_Developer/John_Doe.pdf
data/resume/Data_Engineer/Jane_Smith.pdf
```

## Notes

- Training datasets should have at least 50-100 samples for good ML model performance
- Resume PDFs should be text-based (not scanned images)
- Job descriptions should be comprehensive and detailed
