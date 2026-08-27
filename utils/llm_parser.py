import json
import logging
from typing import Type, TypeVar, Any

logger = logging.getLogger(__name__)

T = TypeVar('T')

def parse_llm_json(raw_text: str, default_factory: Any = None) -> dict:
    """
    Robustly parses JSON from LLM output, handling markdown code fences and trailing text.
    
    Args:
        raw_text: The raw string response from the LLM.
        default_factory: A callable returning a default dict if parsing fails, or a default dict itself.
        
    Returns:
        dict: The parsed JSON object.
    """
    clean = raw_text.strip()
    
    # Remove markdown code block syntax if present
    if clean.startswith("```"):
        # Find the first newline to strip the ```json part
        first_newline = clean.find('\n')
        if first_newline != -1:
            clean = clean[first_newline:].strip()
        # Remove trailing ```
        if clean.endswith("```"):
            clean = clean[:-3].strip()
            
    try:
        result = json.loads(clean)
        if not isinstance(result, dict):
            raise ValueError("Parsed JSON is not a dictionary")
        return result
    except (json.JSONDecodeError, ValueError) as e:
        logger.error(f"Failed to parse LLM JSON: {e}")
        # Do not log the full raw text to avoid leaking PII
        if callable(default_factory):
            return default_factory()
        elif default_factory is not None:
            return default_factory
        return {}
