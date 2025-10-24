"""
Answer Evaluator Agent

Agent responsible for coordinating answer evaluation.
Uses SemanticAnalyzer for concept questions and AIAnalyzer for code questions.
"""

from typing import Dict, Any, List
from .base_agent import BaseAgent
from analyzers.semantic_analyzer import SemanticAnalyzer
from analyzers.ai_analyzer import AIAnalyzer


class AnswerEvaluatorAgent(BaseAgent):
    """Agent for answer evaluation"""
    
    def __init__(self):
        """Initialize answer evaluator agent with analyzers"""
        super().__init__("answer_evaluator")
        self.semantic_analyzer = SemanticAnalyzer()
        self.ai_analyzer = AIAnalyzer("GEMINI_API_KEY_4")
        self.log("Answer Evaluator agent initialized")
    
    def analyze(self, questions: List[Dict[str, Any]], 
                answers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Evaluate all submitted answers
        
        Args:
            questions: List of questions
            answers: List of answers
        
        Returns:
            Dictionary with evaluation results
        """
        self.log(f"Starting evaluation of {len(answers)} answers")
        
        total_score = 0
        evaluated_answers = []
        
        for i, answer_data in enumerate(answers):
            if i >= len(questions):
                break
            
            question = questions[i]
            student_answer = answer_data.get("answer", "")
            
            # Evaluate based on question type
            evaluation = self._evaluate_single_answer(question, student_answer)
            
            evaluated_answers.append({
                "question_id": question.get("id", f"Q{i+1}"),
                "answer": student_answer,
                "score": evaluation["score"],
                "feedback": evaluation["feedback"]
            })
            
            total_score += evaluation["score"]
        
        # Calculate final score
        final_score = round(total_score / len(evaluated_answers), 2) if evaluated_answers else 0
        
        self.log(f"Evaluation complete: final score = {final_score}/10")
        
        return {
            "evaluated_answers": evaluated_answers,
            "final_score": final_score,
            "total_questions": len(evaluated_answers)
        }
    
    def _evaluate_single_answer(self, question: Dict[str, Any], 
                                student_answer: str) -> Dict[str, Any]:
        """
        Evaluate a single answer based on question type
        
        Args:
            question: Question dictionary
            student_answer: Student's answer
        
        Returns:
            Dictionary with score and feedback
        """
        question_type = question.get("type", "concept")
        reference_answer = question.get("reference_answer", "")
        question_text = question.get("question", "")
        
        if question_type == "concept":
            # Use semantic analyzer for concept questions
            result = self.semantic_analyzer.evaluate_concept_answer(
                question_text,
                reference_answer,
                student_answer
            )
        else:
            # Use AI analyzer for code questions
            result = self.ai_analyzer.evaluate_code_answer(
                question_text,
                reference_answer,
                student_answer
            )
        
        return result
