"""
Base Agent Class

Abstract base class for all agents in the hiring system.
Provides common functionality like logging and naming.
"""

import logging
from typing import Any


class BaseAgent:
    """Base class for all agents - provides common functionality"""
    
    def __init__(self, name: str):
        """
        Initialize base agent
        
        Args:
            name: Agent name for logging and identification
        """
        self.name = name
        self.logger = logging.getLogger(f"agent.{name}")
    
    def log(self, message: str, level: str = "info") -> None:
        """
        Log a message with agent name prefix
        
        Args:
            message: Message to log
            level: Log level (info, warning, error, debug)
        """
        log_method = getattr(self.logger, level.lower(), self.logger.info)
        log_method(f"[{self.name}] {message}")
    
    def analyze(self, *args, **kwargs) -> Any:
        """
        Main analysis method - to be implemented by subclasses
        
        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError(f"{self.__class__.__name__} must implement analyze() method")
