import json
from utils.asi1_client import call_asi1
from prompts.system_prompts import INTENT_CLASSIFIER


def classify_intent(description: str) -> dict:
    """
    Layer 1: Classify the citizen's RTI intent.
    Identifies department, ministry, urgency, and applicable RTI sections.

    Args:
        description: Plain-language description of what information the citizen needs

    Returns:
        dict with keys: information_needed, department, ministry, government_level,
                        state_name, rti_section, urgency, urgency_reason, confidence
    """
    raw = call_asi1(
        system_prompt=INTENT_CLASSIFIER,
        user_message=f"Citizen's request: {description}",
        temperature=0.2,  # Low temp for consistent classification
        max_tokens=500,
    )

    try:
        # Strip any markdown code fences if present
        clean = raw.strip().strip("```json").strip("```").strip()
        result = json.loads(clean)
    except json.JSONDecodeError:
        # Fallback: return a low-confidence default so the pipeline doesn't crash
        result = {
            "information_needed": description,
            "department": "Unknown",
            "ministry": "Unknown",
            "government_level": "central",
            "state_name": None,
            "rti_section": "Section 6(1) of RTI Act 2005",
            "urgency": "routine",
            "urgency_reason": "Could not classify automatically",
            "confidence": 0.3,
        }

    # Validate confidence is a proper float
    try:
        result["confidence"] = float(result.get("confidence", 0.5))
    except (ValueError, TypeError):
        result["confidence"] = 0.5

    return result
