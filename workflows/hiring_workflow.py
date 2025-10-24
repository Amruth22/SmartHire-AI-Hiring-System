"""
Hiring Workflow Builder

Defines the staged hiring pipeline with sequential execution.
"""

from graph import HiringGraph
from nodes import (
    resume_parser_node,
    experience_predictor_node,
    resume_scorer_node,
    job_fit_analyzer_node,
    question_generator_node,
    answer_evaluator_node
)


def build_hiring_workflow(max_workers: int = 3) -> HiringGraph:
    """
    Build the main hiring workflow
    
    Stages:
    1. Resume parsing (AI-powered)
    2. Experience prediction (AI-powered)
    3. Resume scoring (AI-powered)
    4. Job fit analysis (AI-powered)
    5. Question generation (AI-powered)
    
    Args:
        max_workers: Maximum number of parallel workers (default: 3)
    
    Returns:
        Compiled HiringGraph ready for execution
    """
    stages = [
        # Stage 1: Parse resume
        [resume_parser_node],
        
        # Stage 2: Predict experience level
        [experience_predictor_node],
        
        # Stage 3: Score resume quality
        [resume_scorer_node],
        
        # Stage 4: Analyze job fit
        [job_fit_analyzer_node],
        
        # Stage 5: Generate interview questions
        [question_generator_node]
    ]
    
    return HiringGraph(stages=stages, max_workers=max_workers, raise_on_error=False)


def build_evaluation_workflow(max_workers: int = 1) -> HiringGraph:
    """
    Build the answer evaluation workflow
    
    This is a separate workflow that runs after user submits answers.
    
    Stages:
    1. Evaluate answers (semantic + AI)
    
    Args:
        max_workers: Maximum number of parallel workers (default: 1)
    
    Returns:
        Compiled HiringGraph ready for execution
    """
    stages = [
        # Stage 1: Evaluate all answers
        [answer_evaluator_node]
    ]
    
    return HiringGraph(stages=stages, max_workers=max_workers, raise_on_error=False)
