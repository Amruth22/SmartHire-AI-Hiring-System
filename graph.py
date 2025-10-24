"""
Hiring Graph - Parallel Execution Engine

Custom graph implementation for executing multi-stage hiring workflows.
Handles orchestration, parallel execution, and state merging.
"""

from typing import Callable, List
from concurrent.futures import ThreadPoolExecutor, as_completed
from state import CandidateState
import traceback
import logging

logger = logging.getLogger("graph")

NodeFunc = Callable[[CandidateState], CandidateState]


class HiringGraph:
    """
    Executes a multi-stage hiring graph with parallel node support
    
    This is PURE orchestration - handles:
    - Stage execution
    - Parallel node execution
    - State merging
    - Error handling
    
    NO business logic here!
    """
    
    def __init__(self, stages: List[List[NodeFunc]], max_workers: int = 3, raise_on_error: bool = False):
        """
        Initialize hiring graph
        
        Args:
            stages: List of stages, each stage is a list of node functions
            max_workers: Maximum number of parallel workers
            raise_on_error: Whether to raise exceptions or continue on error
        """
        self.stages = stages
        self.max_workers = max_workers
        self.raise_on_error = raise_on_error
        logger.info(f"HiringGraph initialized with {len(stages)} stages, max_workers={max_workers}")
    
    def run(self, initial_state: CandidateState) -> CandidateState:
        """
        Execute the hiring workflow graph
        
        Args:
            initial_state: Initial state to start workflow
        
        Returns:
            Final state after all stages complete
        """
        logger.info("=" * 70)
        logger.info("STARTING HIRING WORKFLOW")
        logger.info("=" * 70)
        
        main_state = initial_state
        
        for stage_idx, stage in enumerate(self.stages, start=1):
            if not stage:
                logger.warning(f"Stage {stage_idx} is empty, skipping")
                continue
            
            logger.info(f"Executing Stage {stage_idx} with {len(stage)} node(s)")
            
            # Single node - execute directly
            if len(stage) == 1:
                node = stage[0]
                node_name = getattr(node, "__name__", "unknown")
                logger.info(f"  Executing single node: {node_name}")
                
                try:
                    result = node(main_state)
                    if result:
                        main_state = result
                    logger.info(f"  [OK] {node_name} completed")
                except Exception as e:
                    logger.error(f"  [FAIL] Error in {node_name}: {e}")
                    traceback.print_exc()
                    main_state.errors.append(f"{node_name}: {str(e)}")
                    if self.raise_on_error:
                        raise
                continue
            
            # Multiple nodes - execute in parallel
            logger.info(f"  Executing {len(stage)} nodes in parallel...")
            results = []
            
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Submit all nodes for parallel execution
                futures = {
                    executor.submit(self._safe_run, node, main_state.clone()): node 
                    for node in stage
                }
                
                # Collect results as they complete
                for fut in as_completed(futures):
                    node = futures[fut]
                    node_name = getattr(node, "__name__", "unknown")
                    try:
                        res = fut.result()
                        results.append(res)
                        logger.info(f"  [OK] {node_name} completed")
                    except Exception as e:
                        logger.error(f"  [FAIL] {node_name} failed: {e}")
                        main_state.errors.append(f"{node_name}: {str(e)}")
                        if self.raise_on_error:
                            raise
            
            # Merge all parallel results into main state
            logger.info(f"  Merging {len(results)} parallel results...")
            for res in results:
                try:
                    if res:
                        main_state.merge_from(res)
                except Exception as e:
                    logger.error(f"  Error merging result: {e}")
                    traceback.print_exc()
                    if self.raise_on_error:
                        raise
            
            logger.info(f"Stage {stage_idx} complete")
        
        logger.info("=" * 70)
        logger.info("HIRING WORKFLOW COMPLETE")
        logger.info("=" * 70)
        
        main_state.workflow_complete = True
        return main_state
    
    @staticmethod
    def _safe_run(node: NodeFunc, state_snapshot: CandidateState) -> CandidateState:
        """
        Run a node safely with error handling
        
        Args:
            node: Node function to execute
            state_snapshot: Cloned state for this node
        
        Returns:
            Updated state or original state on error
        """
        node_name = getattr(node, "__name__", "unknown")
        try:
            result = node(state_snapshot)
            return result if result else state_snapshot
        except Exception as e:
            logger.error(f"Node {node_name} failed: {e}")
            # Return state with error metadata
            state_snapshot.errors.append(f"{node_name}: {str(e)}")
            state_snapshot.metadata["node_error"] = {
                "node_name": node_name,
                "error": str(e)
            }
            return state_snapshot
