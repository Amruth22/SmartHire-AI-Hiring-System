"""
SmartHire - Main Application
Streamlit-based web interface for the hiring system
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
from state import CandidateState
from workflows import build_hiring_workflow, build_evaluation_workflow
from utils import extract_text_from_pdf, setup_logging
from config import validate_config

# Setup logging
setup_logging()

# Constants
RESUME_DIR = "data/resume"
JOB_DESC_PATH = "data/job_descriptions.csv"

# Streamlit config
st.set_page_config(
    page_title="SmartHire - AI Hiring System",
    page_icon="briefcase",
    layout="wide"
)

# Validate configuration
try:
    validate_config()
except ValueError as e:
    st.error(f"Configuration Error: {e}")
    st.info("Please set up your .env file with required Gemini API keys")
    st.stop()


# Load job descriptions
@st.cache_data
def load_job_data():
    """Load job descriptions from CSV"""
    if os.path.exists(JOB_DESC_PATH):
        return pd.read_csv(JOB_DESC_PATH)
    return pd.DataFrame()


job_df = load_job_data()

# Initialize session state
if "workflow_state" not in st.session_state:
    st.session_state.workflow_state = None
if "current_questions" not in st.session_state:
    st.session_state.current_questions = []


# Header
st.title("SmartHire - AI-Powered Hiring System")
st.markdown("*Powered by Multi-Agent Architecture with Client Format Pattern*")

# Sidebar for workflow status
with st.sidebar:
    st.header("Workflow Status")
    if st.session_state.workflow_state:
        state = st.session_state.workflow_state
        st.write(f"**Step:** {state.current_step}")
        st.write(f"**Candidate:** {state.candidate_name}")
        
        if state.experience_level:
            st.write(f"**Experience:** {state.experience_level}")
        
        if state.resume_score:
            st.metric("Resume Score", f"{state.resume_score:.1f}/10")
        
        if state.job_fit:
            fit_level = state.job_fit.get('job_fit', 'N/A')
            st.write(f"**Job Fit:** {fit_level}")
        
        if state.errors:
            st.error(f"Errors: {len(state.errors)}")
    else:
        st.info("No workflow running")
    
    st.markdown("---")
    st.markdown("**Architecture:**")
    st.markdown("- Agents (Coordinators)")
    st.markdown("- Analyzers (Tools)")
    st.markdown("- Nodes (Wrappers)")
    st.markdown("- Workflows (Builders)")
    st.markdown("- Graph (Orchestrator)")


# Main tabs
tab1, tab2, tab3 = st.tabs([
    "Resume Analysis & Job Fit",
    "Interview Q&A Session",
    "Results & Evaluation"
])

# Tab 1: Resume Analysis
with tab1:
    st.markdown("### Upload & Analyze Resume")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Get available designations
        designations = []
        if os.path.exists(RESUME_DIR):
            designations = [
                d for d in os.listdir(RESUME_DIR)
                if os.path.isdir(os.path.join(RESUME_DIR, d)) and not d.startswith('.')
            ]
        designation = st.selectbox("Select Designation", [""] + sorted(designations))
    
    with col2:
        # Get resumes for selected designation
        resumes = []
        if designation:
            resume_path = os.path.join(RESUME_DIR, designation)
            if os.path.exists(resume_path):
                resumes = [f for f in os.listdir(resume_path) if f.endswith(".pdf")]
        selected_resume = st.selectbox("Select Resume", [""] + resumes)
    
    with col3:
        # Job titles
        job_titles = []
        if not job_df.empty:
            job_titles = sorted(job_df["job_title"].unique())
        selected_job = st.selectbox("Select Job Role", [""] + job_titles)
    
    # Show job description
    if selected_job and not job_df.empty:
        job_row = job_df[job_df["job_title"] == selected_job]
        if not job_row.empty:
            st.markdown("#### Job Description")
            st.info(job_row.iloc[0]['job_summary'])
            
            with st.expander("Detailed Job Requirements"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Required Skills:**")
                    required_skills = job_row.iloc[0]['required_skills'].split(',')
                    for skill in required_skills:
                        st.write(f"- {skill.strip()}")
                
                with col2:
                    st.write("**Preferred Skills:**")
                    preferred_skills = job_row.iloc[0]['preferred_skills'].split(',')
                    for skill in preferred_skills:
                        st.write(f"- {skill.strip()}")
                
                st.write(f"**Experience Required:** {job_row.iloc[0]['min_required_experience']}-{job_row.iloc[0]['max_required_experience']} years")
                st.write(f"**Difficulty Level:** {job_row.iloc[0]['difficulty_level']}")
    
    # Analysis button
    if not designation or not selected_resume or not selected_job:
        st.warning("Please select all three fields to proceed")
    else:
        if st.button("Start AI Analysis", type="primary"):
            # Extract text from PDF
            full_path = os.path.join(RESUME_DIR, designation, selected_resume)
            
            with st.spinner("Extracting text from PDF..."):
                resume_text = extract_text_from_pdf(full_path)
            
            if "[Error extracting text:" in resume_text:
                st.error(f"Failed to extract text from PDF: {resume_text}")
                st.stop()
            
            # Get job description
            job_row = job_df[job_df["job_title"] == selected_job]
            job_description = job_row.iloc[0]["job_summary"] if not job_row.empty else "No description available"
            
            # Create initial state
            initial_state = CandidateState(
                resume_text=resume_text,
                job_description=job_description,
                job_title=selected_job,
                current_step="start"
            )
            
            # Build and run workflow
            with st.spinner("Running AI analysis workflow..."):
                try:
                    workflow = build_hiring_workflow()
                    result = workflow.run(initial_state)
                    
                    st.session_state.workflow_state = result
                    st.session_state.current_questions = result.questions
                    
                    st.success("Analysis completed successfully!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Analysis failed: {str(e)}")
    
    # Display results
    if st.session_state.workflow_state:
        state = st.session_state.workflow_state
        
        if state.resume_features:
            st.markdown("### AI Evaluation Results")
            
            # Metrics row
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Experience Level", state.experience_level or "N/A")
            with col2:
                resume_score = state.resume_score or 0
                st.metric("Resume Score", f"{resume_score:.1f}/10")
            with col3:
                skills_count = len(state.resume_features.get("skills", []))
                st.metric("Skills Count", skills_count)
            with col4:
                if state.job_fit:
                    fit_result = state.job_fit.get("job_fit", "N/A")
                    st.metric("Job Fit", fit_result)
            
            # Job fit reason
            if state.job_fit:
                fit_reason = state.job_fit.get("reason", "No reason provided")
                st.info(f"**Fit Analysis:** {fit_reason}")
            
            # Detailed features
            with st.expander("View Detailed Resume Features"):
                features = state.resume_features
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Personal Info:**")
                    st.write(f"- Name: {features.get('full_name', 'N/A')}")
                    st.write(f"- Email: {features.get('email', 'N/A')}")
                    st.write(f"- Phone: {features.get('phone', 'N/A')}")
                    
                    st.write("**Education:**")
                    education = features.get('education', {})
                    if isinstance(education, dict):
                        st.write(f"- Degree: {education.get('degree', 'N/A')}")
                        st.write(f"- Major: {education.get('major', 'N/A')}")
                        st.write(f"- University: {education.get('university', 'N/A')}")
                
                with col2:
                    st.write("**Experience:**")
                    st.write(f"- Total Years: {features.get('total_experience_years', 'N/A')}")
                    st.write(f"- Leadership: {features.get('leadership_experience', 'N/A')}")
                    st.write(f"- Research Work: {features.get('has_research_work', 'N/A')}")
                    
                    st.write("**Skills:**")
                    skills = features.get('skills', [])
                    if skills:
                        for skill in skills[:10]:
                            st.write(f"- {skill}")
                        if len(skills) > 10:
                            st.write(f"... and {len(skills) - 10} more")
                
                st.write("**Projects:**")
                projects = features.get('projects', [])
                if projects:
                    for project in projects[:5]:
                        st.write(f"- {project}")
                    if len(projects) > 5:
                        st.write(f"... and {len(projects) - 5} more")
                
                st.write("**Certifications:**")
                certifications = features.get('certifications', [])
                if certifications:
                    for cert in certifications:
                        st.write(f"- {cert}")
                else:
                    st.write("- No certifications extracted")

# Tab 2: Interview Q&A
with tab2:
    st.subheader("AI-Generated Interview Questions")
    
    if not st.session_state.current_questions:
        st.info("Please complete resume analysis in the first tab")
    else:
        questions = st.session_state.current_questions
        st.success(f"Generated {len(questions)} personalized questions")
        
        # Show questions and collect answers
        answers = []
        
        for idx, q in enumerate(questions):
            st.markdown(f"### Question {idx+1}: {q.get('type', 'General').title()} Question")
            st.markdown(f"**{q['question']}**")
            
            # Answer input
            answer_key = f"answer_{idx}"
            student_response = st.text_area(
                "Your Answer:",
                key=answer_key,
                height=120,
                placeholder="Type your detailed answer here..."
            )
            answers.append({"answer": student_response})
            
            # Show reference answer
            with st.expander(f"Reference Answer (for guidance)"):
                st.write(q.get('reference_answer', 'No reference answer available'))
            
            st.markdown("---")
        
        # Submit button
        if st.button("Submit All Answers", type="primary"):
            if all(ans["answer"].strip() for ans in answers):
                # Update state
                state = st.session_state.workflow_state
                state.answers = answers
                state.current_step = "answers_submitted"
                
                with st.spinner("AI is evaluating your answers..."):
                    try:
                        # Build and run evaluation workflow
                        eval_workflow = build_evaluation_workflow()
                        final_state = eval_workflow.run(state)
                        
                        st.session_state.workflow_state = final_state
                        st.success("Answers evaluated successfully!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Evaluation failed: {str(e)}")
            else:
                st.warning("Please answer all questions before submitting")

# Tab 3: Results
with tab3:
    st.subheader("Interview Results & Evaluation")
    
    if not st.session_state.workflow_state or st.session_state.workflow_state.current_step != "completed":
        st.info("Please complete the interview session first")
    else:
        state = st.session_state.workflow_state
        
        # Overall performance
        st.markdown("### Overall Performance")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            final_score = state.final_score or 0
            st.metric("Final Score", f"{final_score:.1f}/10")
        
        with col2:
            resume_score = state.resume_score or 0
            st.metric("Resume Score", f"{resume_score:.1f}/10")
        
        with col3:
            st.metric("Experience", state.experience_level or "N/A")
        
        with col4:
            if state.job_fit:
                fit_score = state.job_fit.get("fit_score", 0)
                st.metric("Job Fit Score", f"{fit_score:.1f}/10")
        
        with col5:
            questions_answered = len(state.answers)
            st.metric("Questions", questions_answered)
        
        # Detailed question analysis
        st.markdown("### Detailed Question Analysis")
        
        if state.answers:
            for i, answer_data in enumerate(state.answers):
                score = answer_data.get("score", 0)
                
                # Color coding
                if score >= 8:
                    score_emoji = "Excellent"
                elif score >= 6:
                    score_emoji = "Good"
                else:
                    score_emoji = "Needs Improvement"
                
                with st.expander(f"Question {i+1} - Score: {score:.1f}/10 ({score_emoji})"):
                    if i < len(st.session_state.current_questions):
                        question = st.session_state.current_questions[i]
                        st.markdown(f"**Question ({question.get('type', 'General')}):**")
                        st.write(question['question'])
                    
                    st.markdown("**Your Answer:**")
                    st.write(answer_data.get('answer', 'No answer provided'))
                    
                    st.markdown(f"**Score: {score:.1f}/10**")
                    st.markdown("**AI Feedback:**")
                    st.info(answer_data.get('feedback', 'No feedback available'))
        
        # Export functionality
        st.markdown("### Export Results")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Generate Summary Report"):
                summary = {
                    "candidate_name": state.candidate_name,
                    "job_title": state.job_title,
                    "resume_score": state.resume_score,
                    "final_score": state.final_score,
                    "experience_level": state.experience_level,
                    "job_fit": state.job_fit,
                    "total_questions": len(state.answers),
                    "evaluation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.json(summary)
        
        with col2:
            # Download detailed results
            detailed_results = {
                "candidate_info": {
                    "name": state.candidate_name,
                    "job_applied": state.job_title,
                    "experience_level": state.experience_level
                },
                "scores": {
                    "resume_score": state.resume_score,
                    "final_score": state.final_score,
                    "job_fit_score": state.job_fit.get("fit_score", 0) if state.job_fit else 0
                },
                "detailed_answers": state.answers,
                "questions": st.session_state.current_questions,
                "timestamp": datetime.now().isoformat()
            }
            
            st.download_button(
                label="Download Full Report (JSON)",
                data=json.dumps(detailed_results, indent=2),
                file_name=f"interview_report_{state.candidate_name.replace(' ', '_')}.json",
                mime="application/json"
            )

# Footer
st.markdown("---")
st.markdown("*Built with Multi-Agent Architecture | Powered by Gemini AI (GenAI) and SBERT*")
