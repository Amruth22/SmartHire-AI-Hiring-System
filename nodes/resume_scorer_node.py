"""
Resume Scorer Node - Simplified Wrapper

Calls ResumeScorerAgent to score resume quality.
"""

from state import CandidateState
from agents.resume_scorer_agent import ResumeScorerAgent

# Create agent instance
agent = ResumeScorerAgent()


def resume_scorer_node(state: CandidateState) -> CandidateState:
    """
    Score resume quality
    
    Args:
        state: Current candidate state
    
    Returns:
        Updated state with resume score
    """
    if not state.resume_features:
        state.errors.append("No resume features available for scoring")
        return state
    
    result = agent.analyze(state.resume_features)
    
    # Update state
    state.resume_score = result.get('resume_score', 5.0)
    state.resume_scoring_results = result
    state.current_step = "resume_scored"
    
    return state
