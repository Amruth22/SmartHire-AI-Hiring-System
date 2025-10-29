"""
Gemini LLM Service

Wrapper for Google's Gemini AI with retry logic and error handling.
"""

import logging
import time
from typing import Optional, Dict, Any
from utils.gemini_client import GeminiClient

logger = logging.getLogger("genai_layer.llm.gemini_service")


class GeminiService:
    """Gemini AI service with advanced features"""
    
    def __init__(self, api_key_name: str = "GEMINI_API_KEY_1", 
                 model: str = "gemini-2.0-flash"):
        """
        Initialize Gemini service
        
        Args:
            api_key_name: Name of API key in config
            model: Model name to use
        """
        self.client = GeminiClient(api_key_name)
        self.model = model
        self.api_key_name = api_key_name
        logger.info(f"Gemini service initialized with {api_key_name}")
    
    def generate(self, prompt: str, max_retries: int = 3, 
                retry_delay: float = 1.0, **kwargs) -> Optional[str]:
        """
        Generate content with retry logic
        
        Args:
            prompt: Input prompt
            max_retries: Maximum number of retries
            retry_delay: Delay between retries (seconds)
            **kwargs: Additional generation parameters
        
        Returns:
            Generated text or None on failure
        """
        if not self.client.is_available():
            logger.error("Gemini client not available")
            return None
        
        for attempt in range(max_retries):
            try:
                response = self.client.generate_content(prompt, **kwargs)
                
                if response:
                    logger.debug(f"Generation successful on attempt {attempt + 1}")
                    return response
                
            except Exception as e:
                logger.warning(f"Generation attempt {attempt + 1} failed: {e}")
                
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (attempt + 1))  # Exponential backoff
                else:
                    logger.error(f"All {max_retries} generation attempts failed")
        
        return None
    
    def generate_json(self, prompt: str, max_retries: int = 3) -> Optional[Dict[str, Any]]:
        """
        Generate JSON response
        
        Args:
            prompt: Input prompt (should request JSON output)
            max_retries: Maximum number of retries
        
        Returns:
            Parsed JSON dictionary or None on failure
        """
        import json
        import re
        
        response = self.generate(prompt, max_retries=max_retries)
        
        if not response:
            return None
        
        try:
            # Clean response
            cleaned = self._clean_json_response(response)
            
            # Parse JSON
            result = json.loads(cleaned)
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed: {e}")
            logger.debug(f"Response: {response[:200]}")
            return None
    
    def _clean_json_response(self, text: str) -> str:
        """
        Clean Gemini response to valid JSON
        
        Args:
            text: Raw response text
        
        Returns:
            Cleaned JSON string
        """
        import re
        
        text = text.strip()
        
        # Remove markdown code blocks
        text = re.sub(r"```json\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"```\s*", "", text)
        
        # Replace single quotes with double quotes
        text = text.replace("'", '"')
        
        # Remove comments
        text = re.sub(r"//.*", "", text)
        
        # Remove trailing commas
        text = re.sub(r",(\s*[}\]])", r"\1", text)
        
        # Ensure proper closing
        if not text.strip().endswith("}") and not text.strip().endswith("]"):
            if "{" in text:
                text += "}"
            elif "[" in text:
                text += "]"
        
        return text
    
    def is_available(self) -> bool:
        """Check if service is available"""
        return self.client.is_available()
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        return {
            "model": self.model,
            "api_key": self.api_key_name,
            "available": self.is_available()
        }


# Service instances for different purposes
_services = {}


def get_gemini_service(api_key_name: str = "GEMINI_API_KEY_1") -> GeminiService:
    """
    Get or create Gemini service instance
    
    Args:
        api_key_name: Name of API key in config
    
    Returns:
        GeminiService instance
    """
    if api_key_name not in _services:
        _services[api_key_name] = GeminiService(api_key_name)
    
    return _services[api_key_name]
