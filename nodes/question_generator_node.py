"""
Question Generator Node - Simplified Wrapper

Calls QuestionGeneratorAgent to generate interview questions.
"""

from state import CandidateState
from agents.question_generator_agent import QuestionGeneratorAgent

# Create agent instance
agent = QuestionGeneratorAgent()


def question_generator_node(state: CandidateState) -> CandidateState:
    """
    Generate personalized interview questions
    
    Args:
        state: Current candidate state
    
    Returns:
        Updated state with generated questions
    """
    if not state.experience_level or not state.resume_features:
        state.errors.append("Missing experience level or resume features for question generation")
        return state
    
    questions = agent.analyze(
        state.experience_level,
        state.job_title,
        state.resume_features
    )
    
    # Update state
    state.questions = questions
    state.current_step = "questions_generated"
    
    return state
