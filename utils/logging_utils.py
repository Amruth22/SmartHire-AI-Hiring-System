"""
Logging Utilities
Configures logging for the SmartHire system
"""

import logging
import os
from datetime import datetime
from config import get_config_value


def setup_logging():
    """
    Setup logging configuration for the application
    
    Creates log directory if it doesn't exist and configures
    both file and console logging.
    """
    # Get configuration
    log_level = get_config_value("LOG_LEVEL", "INFO")
    log_file = get_config_value("LOG_FILE", "logs/smarthire.log")
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    
    # Configure logging format
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # Get log level
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Configure root logger
    logging.basicConfig(
        level=numeric_level,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    # Set specific loggers
    logging.getLogger("graph").setLevel(numeric_level)
    logging.getLogger("agent").setLevel(numeric_level)
    logging.getLogger("analyzer").setLevel(numeric_level)
    logging.getLogger("node").setLevel(numeric_level)
    
    logger = logging.getLogger("logging_utils")
    logger.info(f"Logging configured: level={log_level}, file={log_file}")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance
    
    Args:
        name: Logger name
    
    Returns:
        Logger instance
    """
    return logging.getLogger(name)
