"""
Candidate State - Shared State for Hiring Pipeline

Dataclass-based state management with clone and merge capabilities.
This is ONLY a data structure - NO business logic, NO orchestration logic.
"""

from dataclasses import dataclass, field, asdict, is_dataclass
from typing import List, Dict, Any, Optional
import copy


@dataclass
class CandidateState:
    """
    Shared state for multi-agent hiring pipeline
    
    This is a pure data structure with helper methods for state management.
    All business logic lives in agents/ and nodes/
    All orchestration logic lives in graph.py and workflows/
    """
    
    # Input data
    resume_text: str = ""
    job_description: str = ""
    job_title: str = ""
    candidate_name: str = ""
    
    # Extracted features (from resume parser)
    resume_features: Optional[Dict[str, Any]] = None
    
    # Analysis results (populated by agents)
    experience_level: Optional[str] = None
    experience_prediction_results: Dict[str, Any] = field(default_factory=dict)
    
    resume_score: Optional[float] = None
    resume_scoring_results: Dict[str, Any] = field(default_factory=dict)
    
    job_fit: Optional[Dict[str, Any]] = None
    job_fit_results: Dict[str, Any] = field(default_factory=dict)
    
    # Interview data
    questions: List[Dict[str, Any]] = field(default_factory=list)
    answers: List[Dict[str, Any]] = field(default_factory=list)
    
    # Evaluation results
    final_score: Optional[float] = None
    feedback: Optional[str] = None
    evaluation_results: Dict[str, Any] = field(default_factory=dict)
    
    # Workflow metadata
    current_step: str = "start"
    errors: List[str] = field(default_factory=list)
    workflow_complete: bool = False
    updated_at: str = ""
    
    # Extra metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def clone(self) -> "CandidateState":
        """
        Deep copy for safe parallel execution
        
        Returns:
            Deep copy of the current state
        """
        return copy.deepcopy(self)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert state to dictionary
        
        Returns:
            Dictionary representation of state
        """
        return asdict(self)
    
    def merge_from(self, other: Any, overwrite_scalars: bool = True) -> None:
        """
        Merge another CandidateState or dict into this state
        
        SMART MERGE LOGIC:
        - Initial data fields: REPLACE (don't extend)
        - Result fields: EXTEND or MERGE (accumulate from parallel agents)
        - Dicts: Shallow merge
        - Scalars: Overwrite if allowed
        
        Args:
            other: Another CandidateState instance or dictionary to merge from
            overwrite_scalars: Whether to overwrite scalar values (default: True)
        """
        if other is None:
            return
        
        # Convert to dict if it's a dataclass
        if is_dataclass(other):
            other_dict = asdict(other)
        elif isinstance(other, dict):
            other_dict = other
        else:
            return
        
        # Fields that should be REPLACED, not extended (initial data)
        REPLACE_FIELDS = {'questions', 'answers'}
        
        for key, val in other_dict.items():
            if val is None:
                continue
            
            if not hasattr(self, key):
                # Store unknown keys in metadata
                self.metadata.setdefault("extra", {})[key] = val
                continue
            
            current = getattr(self, key)
            
            # Handle lists with smart logic
            if isinstance(current, list) and isinstance(val, list):
                if key in REPLACE_FIELDS:
                    # REPLACE for initial data (prevent duplicates)
                    setattr(self, key, val)
                else:
                    # EXTEND for other lists (accumulate)
                    current.extend(val)
                    setattr(self, key, current)
                continue
            
            # Merge dicts by updating
            if isinstance(current, dict) and isinstance(val, dict):
                # MERGE dicts (for result fields)
                merged = current.copy()
                merged.update(val)
                setattr(self, key, merged)
                continue
            
            # Merge scalars by overwriting (if allowed and value is not empty)
            if overwrite_scalars and val not in (None, "", [], {}):
                setattr(self, key, val)
