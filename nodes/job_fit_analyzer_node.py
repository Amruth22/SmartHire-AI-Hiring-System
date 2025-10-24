"""
Job Fit Analyzer Node - Simplified Wrapper

Calls JobFitAnalyzerAgent to analyze job compatibility.
"""

from state import CandidateState
from agents.job_fit_analyzer_agent import JobFitAnalyzerAgent

# Create agent instance
agent = JobFitAnalyzerAgent()


def job_fit_analyzer_node(state: CandidateState) -> CandidateState:
    """
    Analyze job fit between candidate and position
    
    Args:
        state: Current candidate state
    
    Returns:
        Updated state with job fit analysis
    """
    if not state.resume_features:
        state.errors.append("No resume features available for job fit analysis")
        return state
    
    result = agent.analyze(
        state.resume_features,
        state.job_description,
        state.job_title
    )
    
    # Update state
    state.job_fit = result
    state.job_fit_results = result
    state.current_step = "job_fit_analyzed"
    
    return state
