"""
Resume Parser Node - Simplified Wrapper

Calls ResumeParserAgent to parse resume and extract features.
"""

from state import CandidateState
from agents.resume_parser_agent import ResumeParserAgent

# Create agent instance
agent = ResumeParserAgent()


def resume_parser_node(state: CandidateState) -> CandidateState:
    """
    Parse resume and extract structured features
    
    Args:
        state: Current candidate state
    
    Returns:
        Updated state with resume features
    """
    result = agent.analyze(state.resume_text)
    
    # Update state
    state.resume_features = result
    state.candidate_name = result.get('full_name', 'Unknown')
    state.current_step = "resume_parsed"
    
    return state
