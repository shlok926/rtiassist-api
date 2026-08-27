from utils.asi1_client import call_asi1
from utils.llm_parser import parse_llm_json
from prompts.system_prompts import AUTHORITY_CLASSIFIER

def classify_problem(problem_description: str) -> dict:
    raw = call_asi1(
        system_prompt=AUTHORITY_CLASSIFIER,
        user_message=f"Citizen Problem:\n{problem_description}",
        temperature=0.1,
        max_tokens=200
    )
    
    def get_fallback():
        return {
            "department": None,
            "ministry": None,
            "government_level": "CENTRAL",
            "state": None,
            "confidence": 0.0
        }
        
    return parse_llm_json(raw, default_factory=get_fallback)
