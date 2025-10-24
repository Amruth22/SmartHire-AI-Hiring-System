"""
Gemini Client - Wrapper for Google Gemini AI
Handles API initialization and content generation
"""

import logging
import google.generativeai as genai
from config import get_config_value

logger = logging.getLogger("gemini_client")


class GeminiClient:
    """Wrapper for Google Gemini AI API"""
    
    def __init__(self, api_key_name: str = "GEMINI_API_KEY_1"):
        """
        Initialize Gemini client
        
        Args:
            api_key_name: Name of the API key in config (default: GEMINI_API_KEY_1)
        """
        self.api_key = get_config_value(api_key_name, "")
        self.model_name = get_config_value("GEMINI_MODEL", "gemini-2.0-flash")
        self.model = None
        
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                
                # Configure generation settings
                generation_config = {
                    "temperature": 0.1,
                    "top_p": 0.8,
                    "top_k": 40,
                    "max_output_tokens": 2048,
                }
                
                self.model = genai.GenerativeModel(
                    self.model_name,
                    generation_config=generation_config
                )
                logger.info(f"Gemini client initialized with model: {self.model_name}")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini client: {e}")
                self.model = None
        else:
            logger.warning(f"No API key found for {api_key_name}")
    
    def generate_content(self, prompt: str, timeout: int = 30) -> str:
        """
        Generate content using Gemini AI
        
        Args:
            prompt: Input prompt
            timeout: Request timeout in seconds
        
        Returns:
            Generated text response
        
        Raises:
            Exception: If generation fails
        """
        if not self.model:
            raise Exception("Gemini model not initialized")
        
        try:
            response = self.model.generate_content(
                prompt,
                request_options={"timeout": timeout}
            )
            return response.text.strip()
        except Exception as e:
            logger.error(f"Content generation failed: {e}")
            raise
    
    def is_available(self) -> bool:
        """Check if Gemini client is available"""
        return self.model is not None
