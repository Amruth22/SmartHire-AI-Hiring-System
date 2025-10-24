"""
Experience Predictor Node - Simplified Wrapper

Calls ExperiencePredictorAgent to predict experience level.
"""

from state import CandidateState
from agents.experience_predictor_agent import ExperiencePredictorAgent

# Create agent instance
agent = ExperiencePredictorAgent()


def experience_predictor_node(state: CandidateState) -> CandidateState:
    """
    Predict candidate experience level
    
    Args:
        state: Current candidate state
    
    Returns:
        Updated state with experience level
    """
    if not state.resume_features:
        state.errors.append("No resume features available for experience prediction")
        return state
    
    result = agent.analyze(state.resume_features)
    
    # Update state
    state.experience_level = result.get('experience_level', 'Mid-Level')
    state.experience_prediction_results = result
    state.current_step = "experience_predicted"
    
    return state
