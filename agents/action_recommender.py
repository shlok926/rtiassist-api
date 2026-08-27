from utils.asi1_client import call_asi1
from utils.llm_parser import parse_llm_json
from prompts.system_prompts import ACTION_RECOMMENDER

def recommend_action(problem_description: str) -> dict:
    """
    Analyzes the citizen's problem and recommends an action.
    Returns a dictionary conforming to the ActionRecommendation schema.
    """
    raw = call_asi1(
        system_prompt=ACTION_RECOMMENDER,
        user_message=f"Citizen's Problem:\n{problem_description}",
        temperature=0.2,
        max_tokens=600,
    )
    
    def get_fallback():
        return {
            "recommended_action": "NEEDS_CLARIFICATION",
            "confidence": 0.0,
            "objective": "Could not automatically determine objective due to parsing error.",
            "reasoning": ["Automated analysis failed. Please review manually or provide more details."],
            "alternative_actions": [],
            "missing_information": ["Please provide more details about your issue."],
            "required_documents": [],
            "urgency": "NORMAL",
            "supported": True,
            "warnings": ["Automated analysis failed."]
        }
        
    result = parse_llm_json(raw, default_factory=get_fallback)
    
    # Deterministic Guardrails
    valid_actions = [
        "RTI", "PUBLIC_GRIEVANCE", "STATUS_FOLLOW_UP", 
        "RECORD_REQUEST", "ADMINISTRATIVE_REPRESENTATION", "FIRST_APPEAL", 
        "OTHER / UNSUPPORTED", "NEEDS_CLARIFICATION"
    ]
    
    if result.get("recommended_action") not in valid_actions:
        result["recommended_action"] = "NEEDS_CLARIFICATION"
        if "Unknown action returned by AI" not in result.get("warnings", []):
            result.setdefault("warnings", []).append("Unknown action returned by AI. Asking for clarification.")
            
    # Hardcode supported logic
    supported_actions = ["RTI", "NEEDS_CLARIFICATION", "FIRST_APPEAL"]
    result["supported"] = result.get("recommended_action") in supported_actions
    
    # Ensure extracted_facts exists
    if "extracted_facts" not in result:
        result["extracted_facts"] = {}
    
    # Confidence normalization
    try:
        conf = float(result.get("confidence", 0.0))
        if not (0.0 <= conf <= 1.0):
            conf = 0.5
        result["confidence"] = conf
    except (ValueError, TypeError):
        result["confidence"] = 0.5
        
    return result
