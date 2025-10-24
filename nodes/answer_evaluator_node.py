"""
Answer Evaluator Node - Simplified Wrapper

Calls AnswerEvaluatorAgent to evaluate candidate answers.
"""

from state import CandidateState
from agents.answer_evaluator_agent import AnswerEvaluatorAgent

# Create agent instance
agent = AnswerEvaluatorAgent()


def answer_evaluator_node(state: CandidateState) -> CandidateState:
    """
    Evaluate candidate answers
    
    Args:
        state: Current candidate state
    
    Returns:
        Updated state with evaluation results
    """
    if not state.questions or not state.answers:
        state.errors.append("Missing questions or answers for evaluation")
        return state
    
    result = agent.analyze(state.questions, state.answers)
    
    # Update state
    state.answers = result.get('evaluated_answers', [])
    state.final_score = result.get('final_score', 0.0)
    state.evaluation_results = result
    state.current_step = "completed"
    
    return state
